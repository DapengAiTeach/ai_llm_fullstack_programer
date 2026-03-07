/**
 * Chatbot SSE 流式聊天模块
 * 处理消息发送、接收和 UI 更新
 * 新增：支持 Mermaid 图表渲染
 */

(function() {
    'use strict';

    // 配置（从 HTML data 属性读取）
    const config = {
        streamUrl: document.getElementById('chat-config')?.dataset.streamUrl || '/chat/stream/',
        csrfToken: document.getElementById('chat-config')?.dataset.csrfToken || ''
    };

    // DOM 元素引用
    const elements = {
        form: document.getElementById('chat-form'),
        input: document.getElementById('message'),
        messagesArea: document.getElementById('messages-area'),
        sendBtn: document.querySelector('.send-btn')
    };

    // 当前 EventSource 实例
    let currentEventSource = null;

    // 防抖定时器（用于 Mermaid 图表渲染）
    let mermaidDebounceTimer = null;

    /**
     * 防抖函数
     * @param {Function} func - 要执行的函数
     * @param {number} wait - 等待时间（毫秒）
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * 渲染 Mermaid 图表（防抖版本）
     */
    const debouncedRenderMermaid = debounce(function(contentEl) {
        if (window.MarkdownRenderer && typeof window.MarkdownRenderer.renderMermaidCharts === 'function') {
            try {
                window.MarkdownRenderer.renderMermaidCharts(contentEl);
            } catch (e) {
                console.warn('Mermaid render error:', e);
            }
        }
    }, 500);

    /**
     * 初始化
     */
    function init() {
        if (!elements.form || !elements.input) {
            console.error('Chatbot: 找不到必要的 DOM 元素');
            return;
        }

        // 绑定表单提交事件
        elements.form.addEventListener('submit', handleFormSubmit);

        // 初始化输入框高度
        autoResizeTextarea();
        elements.input.addEventListener('input', autoResizeTextarea);
        
        // 绑定消息复制按钮事件（事件委托）
        bindMessageCopyButton();
        
        // 绑定消息图片下载按钮事件（事件委托）
        bindMessageDownloadButton();

        console.log('Chatbot: 初始化完成');
    }

    /**
     * 绑定消息整体复制按钮事件
     */
    function bindMessageCopyButton() {
        elements.messagesArea.addEventListener('click', function(e) {
            const btn = e.target.closest('.message-copy-btn');
            if (!btn) return;
            
            // 找到消息容器
            const messageEl = btn.closest('.message.ai');
            if (!messageEl) return;
            
            // 获取 Markdown 内容
            const markdownContent = messageEl.dataset.markdown;
            if (!markdownContent) {
                console.warn('Chatbot: 未找到 Markdown 内容');
                return;
            }
            
            // 复制到剪贴板
            copyToClipboard(markdownContent).then(function(success) {
                if (success) {
                    showMessageCopySuccess(btn);
                }
            });
        });
    }

    /**
     * 绑定消息图片下载按钮事件
     */
    function bindMessageDownloadButton() {
        elements.messagesArea.addEventListener('click', function(e) {
            const btn = e.target.closest('.message-download-img-btn');
            if (!btn) return;
            
            // 找到消息容器
            const messageEl = btn.closest('.message.ai');
            if (!messageEl) return;
            
            // 找到消息中的第一张图片
            const img = messageEl.querySelector('.message-content img, .image-wrapper img');
            if (!img) {
                console.warn('Chatbot: 未找到可下载的图片');
                return;
            }
            
            const src = img.getAttribute('src');
            if (!src) return;
            
            // 提取文件名
            let filename = 'image.png';
            const alt = img.getAttribute('alt') || '';
            if (alt) {
                filename = alt.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_') + '.png';
            }
            if (src.includes('/')) {
                const lastPart = src.substring(src.lastIndexOf('/') + 1);
                if (lastPart && lastPart.includes('.')) {
                    filename = lastPart.split('?')[0];
                }
            }
            
            // 下载图片
            const success = downloadImage(src, filename);
            if (success) {
                // 显示成功反馈
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="bi bi-check-lg"></i><span>已下载</span>';
                btn.classList.add('downloaded');
                
                setTimeout(function() {
                    btn.innerHTML = originalHTML;
                    btn.classList.remove('downloaded');
                }, 2000);
            }
        });
    }

    /**
     * 下载图片
     * @param {string} url - 图片地址
     * @param {string} filename - 文件名
     * @returns {boolean} - 是否成功
     */
    function downloadImage(url, filename) {
        // 处理 Base64 图片
        if (url.startsWith('data:image')) {
            try {
                const link = document.createElement('a');
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                return true;
            } catch (e) {
                console.warn('Base64 download failed:', e);
                window.open(url, '_blank');
                return false;
            }
        }

        // 普通 URL 下载
        try {
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            return true;
        } catch (e) {
            console.warn('Direct download failed:', e);
            window.open(url, '_blank');
            return false;
        }
    }

    /**
     * 复制文本到剪贴板
     * @param {string} text - 要复制的文本
     * @returns {Promise<boolean>} - 是否复制成功
     */
    function copyToClipboard(text) {
        return new Promise(function(resolve) {
            // 优先使用现代 Clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function() {
                    resolve(true);
                }).catch(function(err) {
                    console.warn('Clipboard API failed:', err);
                    resolve(fallbackCopyToClipboard(text));
                });
            } else {
                resolve(fallbackCopyToClipboard(text));
            }
        });
    }

    /**
     * 降级复制方案（使用 execCommand）
     * @param {string} text - 要复制的文本
     * @returns {boolean} - 是否复制成功
     */
    function fallbackCopyToClipboard(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        textarea.style.top = '0';
        document.body.appendChild(textarea);
        
        let success = false;
        try {
            textarea.select();
            textarea.setSelectionRange(0, 99999);
            success = document.execCommand('copy');
        } catch (e) {
            console.warn('execCommand copy failed:', e);
        }
        
        document.body.removeChild(textarea);
        return success;
    }

    /**
     * 显示消息复制成功反馈
     * @param {HTMLElement} button - 复制按钮元素
     */
    function showMessageCopySuccess(button) {
        const icon = button.querySelector('i');
        const textSpan = button.querySelector('span');
        if (!icon) return;
        
        const originalHTML = button.innerHTML;
        button.classList.add('copied');
        button.innerHTML = '<i class="bi bi-check-lg"></i><span>已复制</span>';
        button.disabled = true;
        
        setTimeout(function() {
            button.classList.remove('copied');
            button.innerHTML = originalHTML;
            button.disabled = false;
        }, 2000);
    }

    /**
     * 处理表单提交
     */
    function handleFormSubmit(event) {
        event.preventDefault();

        const message = elements.input.value.trim();
        if (!message) return;

        // 禁用输入和按钮
        setInputEnabled(false);

        // 添加用户消息到界面
        addUserMessage(message);

        // 清空输入框
        elements.input.value = '';
        autoResizeTextarea();

        // 添加 AI 消息占位并建立 SSE 连接
        const aiMessageEl = addAIMessagePlaceholder();
        connectStream(message, aiMessageEl);
    }

    /**
     * 建立 SSE 连接
     */
    function connectStream(message, aiMessageEl) {
        // 关闭之前的连接（如果有）
        if (currentEventSource) {
            currentEventSource.close();
        }

        // 构建 URL（GET 方式传递消息）
        const url = `${config.streamUrl}?message=${encodeURIComponent(message)}`;

        // 创建 EventSource
        currentEventSource = new EventSource(url);

        let accumulatedContent = '';

        currentEventSource.onopen = function() {
            // 连接成功，移除"正在思考"状态
            const placeholder = aiMessageEl.querySelector('.typing-indicator');
            if (placeholder) placeholder.remove();
        };

        currentEventSource.onmessage = function(event) {
            const data = event.data;

            // 检查是否结束
            if (data === '[DONE]') {
                currentEventSource.close();
                currentEventSource = null;
                setInputEnabled(true);
                
                // 消息结束时，立即渲染 Mermaid 图表（不等待防抖）
                const contentEl = aiMessageEl.querySelector('.message-content');
                if (contentEl && window.MarkdownRenderer && typeof window.MarkdownRenderer.renderMermaidCharts === 'function') {
                    try {
                        window.MarkdownRenderer.renderMermaidCharts(contentEl);
                    } catch (e) {
                        console.warn('Final Mermaid render error:', e);
                    }
                }
                
                // 检测是否有图片，有则显示下载按钮
                updateDownloadButtonVisibility(aiMessageEl);
                return;
            }

            // 检查是否错误
            if (data.startsWith('[ERROR]')) {
                const errorMsg = data.substring(7).trim();
                showError(errorMsg, aiMessageEl);
                currentEventSource.close();
                currentEventSource = null;
                setInputEnabled(true);
                return;
            }

            // 解码并追加内容
            const decodedContent = decodeSSEContent(data);
            accumulatedContent += decodedContent;
            updateAIMessage(aiMessageEl, accumulatedContent);
        };

        currentEventSource.onerror = function(error) {
            console.error('Chatbot: SSE 连接错误', error);
            showError('连接异常，请重试', aiMessageEl);
            currentEventSource.close();
            currentEventSource = null;
            setInputEnabled(true);
        };
    }

    /**
     * 添加用户消息到界面
     */
    function addUserMessage(content) {
        const html = `
            <div class="message user">
                <div class="message-avatar">👤</div>
                <div>
                    <div class="message-content">${escapeHtml(content)}</div>
                    <div class="message-time">刚刚</div>
                </div>
            </div>
        `;
        appendMessage(html);
    }

    /**
     * 添加 AI 消息占位符
     */
    function addAIMessagePlaceholder() {
        const tempId = 'ai-msg-' + Date.now();
        const html = `
            <div class="message ai" id="${tempId}">
                <div class="message-avatar">🤖</div>
                <div class="message-wrapper">
                    <div class="message-content markdown-body">
                        <span class="typing-indicator">正在思考<span>.</span><span>.</span><span>.</span></span>
                    </div>
                    <div class="message-actions">
                        <span class="message-time">刚刚</span>
                        <div class="message-action-buttons">
                            <button type="button" class="message-download-img-btn" title="下载图片" aria-label="下载图片" style="display: none;">
                                <i class="bi bi-download"></i>
                                <span>下载图片</span>
                            </button>
                            <button type="button" class="message-copy-btn" title="复制完整回复" aria-label="复制完整回复">
                                <i class="bi bi-clipboard"></i>
                                <span>复制</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        appendMessage(html);
        return document.getElementById(tempId);
    }

    /**
     * 更新 AI 消息内容
     */
    function updateAIMessage(element, content) {
        const contentEl = element.querySelector('.message-content');
        if (contentEl) {
            // 使用 Markdown 渲染器将内容渲染为 HTML
            if (window.MarkdownRenderer && typeof window.MarkdownRenderer.render === 'function') {
                contentEl.innerHTML = window.MarkdownRenderer.render(content);
                
                // 增量高亮新出现的代码块
                if (typeof window.MarkdownRenderer.highlightNewBlocks === 'function') {
                    window.MarkdownRenderer.highlightNewBlocks(contentEl);
                }
                
                // 为代码块添加复制按钮
                if (typeof window.MarkdownRenderer.addCopyButtons === 'function') {
                    window.MarkdownRenderer.addCopyButtons(contentEl);
                }
                
                // 处理图片添加下载功能
                if (typeof window.MarkdownRenderer.processImages === 'function') {
                    window.MarkdownRenderer.processImages(contentEl);
                }
                
                // 延迟渲染 Mermaid 图表（使用防抖避免频繁渲染）
                debouncedRenderMermaid(contentEl);
                
                // 存储原始 Markdown 内容到 data 属性
                element.dataset.markdown = content;
            } else {
                // 降级方案：直接显示纯文本
                contentEl.textContent = content;
                element.dataset.markdown = content;
            }
            scrollToBottom();
        }
    }

    /**
     * 显示错误信息
     */
    function showError(message, aiMessageEl) {
        const contentEl = aiMessageEl.querySelector('.message-content');
        if (contentEl) {
            contentEl.innerHTML = `<span class="text-danger">⚠️ ${escapeHtml(message)}</span>`;
        }
    }

    /**
     * 追加消息到消息区域
     */
    function appendMessage(html) {
        // 移除欢迎消息（如果有）
        const welcomeMsg = elements.messagesArea.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }

        // 插入新消息
        elements.messagesArea.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

    /**
     * 滚动到底部
     */
    function scrollToBottom() {
        if (elements.messagesArea) {
            elements.messagesArea.scrollTop = elements.messagesArea.scrollHeight;
        }
    }

    /**
     * 设置输入状态
     */
    function setInputEnabled(enabled) {
        elements.input.disabled = !enabled;
        if (elements.sendBtn) {
            elements.sendBtn.disabled = !enabled;
        }
    }

    /**
     * 自动调整输入框高度
     */
    function autoResizeTextarea() {
        if (!elements.input) return;
        elements.input.style.height = 'auto';
        elements.input.style.height = elements.input.scrollHeight + 'px';
    }

    /**
     * 解码 SSE 内容（处理转义字符）
     */
    function decodeSSEContent(content) {
        // 还原换行符转义
        return content.replace(/\\n/g, '\n');
    }

    /**
     * HTML 转义
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * 更新下载按钮可见性（检测消息中是否有图片）
     * @param {HTMLElement} messageEl - 消息元素
     */
    function updateDownloadButtonVisibility(messageEl) {
        if (!messageEl) return;
        
        const contentEl = messageEl.querySelector('.message-content');
        const downloadBtn = messageEl.querySelector('.message-download-img-btn');
        
        if (!contentEl || !downloadBtn) return;
        
        // 检测是否有图片（包括普通img和包装后的图片）
        const hasImage = contentEl.querySelector('img, .image-wrapper') !== null;
        
        if (hasImage) {
            downloadBtn.style.display = 'flex';
        } else {
            downloadBtn.style.display = 'none';
        }
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
