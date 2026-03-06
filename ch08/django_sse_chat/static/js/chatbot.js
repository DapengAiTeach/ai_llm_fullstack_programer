/**
 * Chatbot SSE 流式聊天模块
 * 处理消息发送、接收和 UI 更新
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

        console.log('Chatbot: 初始化完成');
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
                <div>
                    <div class="message-content">
                        <span class="typing-indicator">正在思考<span>.</span><span>.</span><span>.</span></span>
                    </div>
                    <div class="message-time">刚刚</div>
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
            // 将换行符转换为 <br> 标签
            contentEl.innerHTML = escapeHtml(content).replace(/\\n/g, '<br>');
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

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
