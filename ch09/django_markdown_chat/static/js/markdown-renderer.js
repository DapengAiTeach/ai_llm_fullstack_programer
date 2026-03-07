/**
 * Markdown 渲染器模块
 * 封装 marked.js 配置和 highlight.js 代码高亮
 * 新增：支持 Mermaid 图表渲染（DOM 后处理方案）
 */

(function() {
    'use strict';

    // 语言别名映射
    const languageAliases = {
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'sh': 'bash',
        'shell': 'bash',
        'yml': 'yaml',
        'html': 'xml',
        'htm': 'xml'
    };

    // Mermaid 图表渲染状态跟踪
    var renderedMermaidCharts = new WeakSet();

    // HTML 转义函数
    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&',
            '<': '<',
            '>': '>',
            '"': '"',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // 检查 highlight.js 是否已加载
    function isHighlightReady() {
        return typeof hljs !== 'undefined';
    }

    // 检查 marked 是否已加载
    function isMarkedReady() {
        return typeof marked !== 'undefined';
    }

    // 检查 Mermaid 是否已加载
    function isMermaidReady() {
        return typeof mermaid !== 'undefined';
    }

    // 代码高亮函数
    function highlightCode(code, lang) {
        if (!isHighlightReady()) {
            return escapeHtml(code);
        }

        // 处理语言别名
        if (lang && languageAliases[lang]) {
            lang = languageAliases[lang];
        }

        // 如果指定了语言且该语言已注册
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(code, { language: lang }).value;
            } catch (e) {
                console.warn('Highlight error for language:', lang, e);
            }
        }

        // 尝试自动检测
        try {
            return hljs.highlightAuto(code).value;
        } catch (e) {
            console.warn('Highlight auto error:', e);
        }

        // 返回转义的代码
        return escapeHtml(code);
    }

    // 初始化 Mermaid
    function initMermaid() {
        if (!isMermaidReady()) {
            console.warn('mermaid.js is not loaded, chart rendering will be disabled');
            return false;
        }

        try {
            mermaid.initialize({
                startOnLoad: false,           // 不自动渲染，由我们手动控制
                theme: 'default',             // 主题：default, dark, forest, neutral
                securityLevel: 'strict',      // 安全级别，防止XSS
                flowchart: {
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis'
                },
                sequence: {
                    useMaxWidth: true
                },
                gantt: {
                    useMaxWidth: true
                }
            });
            return true;
        } catch (e) {
            console.error('Mermaid initialization error:', e);
            return false;
        }
    }

    // 初始化 marked.js
    function initMarked() {
        if (!isMarkedReady()) {
            console.error('marked.js is not loaded!');
            return false;
        }

        // 配置 marked.js 选项（不使用自定义 renderer，采用后处理方案）
        marked.setOptions({
            // 启用 GitHub 风格的换行
            breaks: true,
            // 启用 GitHub 风格的 Markdown
            gfm: true,
            // 代码高亮回调函数
            highlight: function(code, lang) {
                return highlightCode(code, lang);
            },
            // 为代码块添加语言类名
            langPrefix: 'hljs language-',
            // pedantic 模式
            pedantic: false,
            // 智能列表
            smartLists: true,
            // 智能引号
            smartypants: false,
            // 标题添加锚点
            headerIds: true,
            headerPrefix: 'heading-'
        });

        return true;
    }

    // 【新增】转换 Mermaid 代码块（DOM 后处理方案）
    function convertMermaidBlocks(html) {
        if (!html) return '';

        // 匹配 <pre><code class="language-mermaid">...</code></pre>
        // 注意：marked 可能已经转义了 HTML 实体
        return html.replace(
            /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/gi,
            function(match, codeContent) {
                // 解码 HTML 实体（因为 marked 已经转义了特殊字符）
                var decodedCode = codeContent
                    .replace(/&/g, '&')
                    .replace(/</g, '<')
                    .replace(/>/g, '>')
                    .replace(/"/g, '"')
                    .replace(/&#039;/g, "'");
                
                // 生成唯一ID
                var id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
                
                // 返回 mermaid 容器（编码后的代码存入 data-code）
                return '<div class="mermaid-container" id="' + id + '" data-code="' + escapeHtml(decodedCode) + '"></div>';
            }
        );
    }

    // 简单的 HTML 清理函数（防止 XSS）
    function sanitizeHtml(html) {
        if (!html) return '';

        // 允许的 HTML 标签列表
        var allowedTags = {
            'p': [], 'br': [], 'hr': [],
            'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [],
            'ul': [], 'ol': [], 'li': [],
            'strong': [], 'b': [], 'em': [], 'i': [], 'del': [], 's': [], 'code': ['class'],
            'pre': ['class'], 'blockquote': [],
            'a': ['href', 'title', 'target'], 'img': ['src', 'alt', 'title'],
            'table': [], 'thead': [], 'tbody': [], 'tr': [], 'th': [], 'td': [],
            'div': ['class', 'id', 'data-code'], 'span': ['class']
        };

        // 危险的 URL 协议
        var dangerousProtocols = /^javascript:|data:text\/html|vbscript:/i;

        // 使用正则表达式清理 HTML
        var sanitized = html.replace(/<\/?([a-z0-9]+)([^>]*)>/gi, function(match, tag, attrs) {
            tag = tag.toLowerCase();
            
            if (!allowedTags.hasOwnProperty(tag)) {
                return '';
            }

            var allowedAttrs = allowedTags[tag];
            var cleanAttrs = '';
            
            if (allowedAttrs && allowedAttrs.length > 0) {
                attrs.replace(/([a-z0-9-]+)="([^"]*)"/gi, function(attrMatch, attrName, attrValue) {
                    attrName = attrName.toLowerCase();
                    
                    if (allowedAttrs.indexOf(attrName) !== -1) {
                        if ((attrName === 'href' || attrName === 'src') && attrValue) {
                            if (dangerousProtocols.test(attrValue)) {
                                return;
                            }
                        }
                        cleanAttrs += ' ' + attrName + '="' + attrValue.replace(/"/g, '"') + '"';
                    }
                });
            }

            return '<' + (match.charAt(1) === '/' ? '/' : '') + tag + cleanAttrs + '>';
        });

        return sanitized;
    }

    // 初始化状态
    var isInitialized = false;
    var isMermaidInitialized = false;
    
    // 已高亮代码块记录（用于增量高亮）
    var highlightedBlocks = new WeakSet();
    
    // 已添加复制按钮的代码块记录
    var processedForCopy = new WeakSet();
    
    // 已处理的图片记录
    var processedImages = new WeakSet();

    // 初始化函数
    function init() {
        if (isInitialized) return true;

        if (!isMarkedReady()) {
            console.error('marked.js is required but not loaded');
            return false;
        }

        if (!isHighlightReady()) {
            console.warn('highlight.js is not loaded, code highlighting will be disabled');
        }

        initMarked();
        isMermaidInitialized = initMermaid();
        isInitialized = true;
        return true;
    }
    
    /**
     * 对容器中的新代码块进行增量高亮
     * @param {HTMLElement} container - 包含代码块的容器元素
     */
    function highlightNewBlocks(container) {
        if (!isHighlightReady() || !container) {
            return;
        }
        
        // 查找所有未高亮的代码块（跳过 mermaid 容器中的）
        var codeBlocks = container.querySelectorAll('pre code:not(.hljs)');
        
        codeBlocks.forEach(function(block) {
            // 跳过已处理的块
            if (highlightedBlocks.has(block)) {
                return;
            }
            
            // 跳过 mermaid 代码块（保险起见，虽然应该已经被转换了）
            if (block.classList.contains('language-mermaid')) {
                return;
            }
            
            try {
                hljs.highlightElement(block);
                highlightedBlocks.add(block);
            } catch (e) {
                console.warn('Highlight error:', e);
            }
        });
    }

    /**
     * 渲染单个 Mermaid 图表
     * @param {HTMLElement} container - 图表容器元素
     * @param {string} code - Mermaid 代码
     */
    function renderSingleMermaidChart(container, code) {
        if (!isMermaidReady() || !container) {
            return false;
        }

        // 检查是否已渲染
        if (renderedMermaidCharts.has(container)) {
            return true;
        }

        try {
            // 清空容器
            container.innerHTML = '';
            
            // 生成唯一ID
            var id = 'mermaid-svg-' + Math.random().toString(36).substr(2, 9);
            
            // 使用 mermaid.render 渲染
            mermaid.render(id, code).then(function(result) {
                container.innerHTML = result.svg;
                container.classList.add('mermaid-rendered');
                renderedMermaidCharts.add(container);
                
                // 【可选】为图表添加复制按钮
                addMermaidCopyButton(container, code);
                
                // 为图表添加下载按钮
                addMermaidDownloadButton(container);
            }).catch(function(error) {
                // 渲染失败时显示错误信息
                console.warn('Mermaid render error:', error);
                container.innerHTML = '<div class="mermaid-error">图表渲染失败，请检查语法</div>';
            });
            
            return true;
        } catch (e) {
            console.warn('Mermaid render exception:', e);
            return false;
        }
    }

    /**
     * 【新增】为 Mermaid 图表添加复制按钮
     * @param {HTMLElement} container - 图表容器
     * @param {string} code - Mermaid 源代码
     */
    function addMermaidCopyButton(container, code) {
        // 创建复制按钮
        var button = document.createElement('button');
        button.className = 'mermaid-copy-btn';
        button.setAttribute('type', 'button');
        button.setAttribute('title', '复制图表源码');
        button.innerHTML = '<i class="bi bi-copy"></i>';
        
        // 绑定点击事件
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            copyToClipboard(code).then(function(success) {
                if (success) {
                    var originalHTML = button.innerHTML;
                    button.innerHTML = '<i class="bi bi-check-lg"></i>';
                    button.classList.add('copied');
                    
                    setTimeout(function() {
                        button.innerHTML = originalHTML;
                        button.classList.remove('copied');
                    }, 2000);
                }
            });
        });
        
        // 添加到容器
        container.style.position = 'relative';
        container.appendChild(button);
    }

    /**
     * 【新增】为 Mermaid 图表添加下载按钮
     * @param {HTMLElement} container - 图表容器
     */
    function addMermaidDownloadButton(container) {
        // 创建下载按钮
        var button = document.createElement('button');
        button.className = 'mermaid-download-btn';
        button.setAttribute('type', 'button');
        button.setAttribute('title', '下载图表为 SVG');
        button.innerHTML = '<i class="bi bi-download"></i>';
        
        // 绑定点击事件
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // 获取 SVG 元素
            var svg = container.querySelector('svg');
            if (!svg) {
                console.warn('No SVG found in container');
                return;
            }
            
            try {
                // 克隆 SVG 以修改样式
                var clonedSvg = svg.cloneNode(true);
                
                // 确保 SVG 有 xmlns 命名空间
                if (!clonedSvg.getAttribute('xmlns')) {
                    clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
                }
                
                // 序列化 SVG
                var serializer = new XMLSerializer();
                var svgString = serializer.serializeToString(clonedSvg);
                
                // 添加 XML 声明
                svgString = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + svgString;
                
                // 创建 Blob 并下载 SVG
                var blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
                var url = URL.createObjectURL(blob);
                var link = document.createElement('a');
                link.href = url;
                link.download = 'mermaid-chart-' + Date.now() + '.svg';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                // 显示成功反馈
                var originalHTML = button.innerHTML;
                button.innerHTML = '<i class="bi bi-check-lg"></i>';
                button.classList.add('downloaded');
                
                setTimeout(function() {
                    button.innerHTML = originalHTML;
                    button.classList.remove('downloaded');
                }, 2000);
            } catch (e) {
                console.warn('Mermaid download error:', e);
            }
        });
        
        // 添加到容器
        container.appendChild(button);
    }
    

    /**
     * 渲染容器中的所有 Mermaid 图表
     * @param {HTMLElement} container - 包含图表的容器元素
     */
    function renderMermaidCharts(container) {
        if (!isMermaidReady() || !container) {
            return;
        }

        // 查找所有未渲染的 mermaid 容器
        var mermaidContainers = container.querySelectorAll('.mermaid-container:not(.mermaid-rendered)');
        
        mermaidContainers.forEach(function(element) {
            // 获取代码
            var code = element.getAttribute('data-code');
            if (!code) {
                return;
            }
            
            // 解码 HTML 实体
            var decodedCode = code.replace(/&/g, '&')
                                  .replace(/</g, '<')
                                  .replace(/>/g, '>')
                                  .replace(/"/g, '"')
                                  .replace(/&#039;/g, "'");
            
            // 渲染图表
            renderSingleMermaidChart(element, decodedCode);
        });
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
                    // 降级到传统方法
                    resolve(fallbackCopyToClipboard(text));
                });
            } else {
                // 使用降级方案
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
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        textarea.style.top = '0';
        document.body.appendChild(textarea);
        
        var success = false;
        try {
            textarea.select();
            textarea.setSelectionRange(0, 99999); // 兼容移动设备
            success = document.execCommand('copy');
        } catch (e) {
            console.warn('execCommand copy failed:', e);
        }
        
        document.body.removeChild(textarea);
        return success;
    }

    /**
     * 显示复制成功反馈
     * @param {HTMLElement} button - 复制按钮元素
     */
    function showCopySuccess(button) {
        var originalHTML = button.innerHTML;
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
     * 从代码块元素中提取纯文本
     * @param {HTMLElement} preElement - pre 元素
     * @returns {string} - 代码文本
     */
    function getCodeText(preElement) {
        var codeElement = preElement.querySelector('code');
        if (!codeElement) return '';
        
        // 获取文本内容，处理 HTML 实体
        var text = codeElement.textContent || codeElement.innerText || '';
        return text.replace(/\n$/, ''); // 移除末尾多余换行
    }

    /**
     * 为容器中的代码块添加复制按钮
     * @param {HTMLElement} container - 包含代码块的容器元素
     */
    function addCopyButtons(container) {
        if (!container) return;
        
        // 查找所有 pre 元素
        var preBlocks = container.querySelectorAll('pre');
        
        preBlocks.forEach(function(pre) {
            // 跳过已处理的块
            if (processedForCopy.has(pre)) {
                return;
            }
            
            // 检查是否有代码内容
            var codeText = getCodeText(pre);
            if (!codeText.trim()) {
                return;
            }
            
            // 创建复制按钮
            var button = document.createElement('button');
            button.className = 'code-copy-btn';
            button.setAttribute('type', 'button');
            button.setAttribute('aria-label', '复制代码');
            button.innerHTML = '<i class="bi bi-copy"></i><span>复制</span>';
            
            // 绑定点击事件
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                var text = getCodeText(pre);
                copyToClipboard(text).then(function(success) {
                    if (success) {
                        showCopySuccess(button);
                    } else {
                        console.warn('Copy failed');
                    }
                });
            });
            
            // 添加到 pre 元素
            pre.appendChild(button);
            processedForCopy.add(pre);
        });
    }

    /**
     * 下载图片
     * @param {string} url - 图片地址
     * @param {string} filename - 文件名
     */
    function downloadImage(url, filename) {
        // 处理 Base64 图片
        if (url.startsWith('data:image')) {
            try {
                var link = document.createElement('a');
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                return true;
            } catch (e) {
                console.warn('Base64 download failed:', e);
                return false;
            }
        }

        // 普通 URL 下载
        var link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.target = '_blank';
        
        // 尝试下载
        try {
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            return true;
        } catch (e) {
            console.warn('Direct download failed:', e);
            // 降级：打开新窗口
            window.open(url, '_blank');
            return false;
        }
    }

    /**
     * 处理容器中的图片，添加下载功能
     * @param {HTMLElement} container - 包含图片的容器元素
     */
    function processImages(container) {
        if (!container) return;
        
        // 查找所有图片
        var images = container.querySelectorAll('img');
        
        images.forEach(function(img) {
            // 跳过已处理的图片
            if (processedImages.has(img)) {
                return;
            }
            
            // 跳过 Mermaid 图表中的 SVG（它们已经是渲染后的内容）
            if (img.closest('.mermaid-container') || img.closest('.mermaid-rendered')) {
                return;
            }
            
            try {
                var src = img.getAttribute('src');
                var alt = img.getAttribute('alt') || 'image';
                if (!src) return;
                
                // 提取文件名
                var filename = alt.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_') + '.png';
                if (src.includes('/')) {
                    var lastPart = src.substring(src.lastIndexOf('/') + 1);
                    if (lastPart && lastPart.includes('.')) {
                        filename = lastPart.split('?')[0]; // 移除查询参数
                    }
                }
                
                // 创建包装容器
                var wrapper = document.createElement('div');
                wrapper.className = 'image-wrapper';
                
                // 克隆图片
                var newImg = img.cloneNode(true);
                
                // 创建下载按钮
                var button = document.createElement('button');
                button.className = 'image-download-btn';
                button.setAttribute('type', 'button');
                button.setAttribute('title', '下载图片');
                button.innerHTML = '<i class="bi bi-download"></i>';
                
                // 绑定下载事件
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    var success = downloadImage(src, filename);
                    if (success) {
                        // 显示成功反馈
                        var originalHTML = button.innerHTML;
                        button.innerHTML = '<i class="bi bi-check-lg"></i>';
                        button.classList.add('copied');
                        
                        setTimeout(function() {
                            button.innerHTML = originalHTML;
                            button.classList.remove('copied');
                        }, 2000);
                    }
                });
                
                // 组装结构
                wrapper.appendChild(newImg);
                wrapper.appendChild(button);
                
                // 替换原图片
                img.parentNode.replaceChild(wrapper, img);
                
                // 标记为已处理（标记新图片）
                processedImages.add(newImg);
            } catch (e) {
                console.warn('Image processing error:', e);
            }
        });
    }

    /**
     * 渲染 Markdown 为 HTML
     * @param {string} text - Markdown 文本
     * @param {Object} options - 选项
     * @param {boolean} options.sanitize - 是否清理 HTML（默认 true）
     * @returns {string} - 渲染后的 HTML
     */
    function renderMarkdown(text, options) {
        options = options || {};
        var doSanitize = options.sanitize !== false;

        if (!text || typeof text !== 'string') {
            return '';
        }

        // 确保已初始化
        if (!isInitialized) {
            if (!init()) {
                return escapeHtml(text).replace(/\n/g, '<br>');
            }
        }

        try {
            // 1. 解析 Markdown
            var html = marked.parse(text);

            // 2. 清理 HTML（XSS 防护）
            if (doSanitize) {
                html = sanitizeHtml(html);
            }

            // 3. 【新增】转换 mermaid 代码块（DOM 后处理方案）
            html = convertMermaidBlocks(html);

            return html;
        } catch (e) {
            console.error('Markdown render error:', e);
            return escapeHtml(text).replace(/\n/g, '<br>');
        }
    }

    // 导出到全局作用域
    window.MarkdownRenderer = {
        render: renderMarkdown,
        init: init,
        escapeHtml: escapeHtml,
        isReady: function() { return isInitialized; },
        isMermaidReady: function() { return isMermaidInitialized; },
        highlightNewBlocks: highlightNewBlocks,
        addCopyButtons: addCopyButtons,
        renderMermaidCharts: renderMermaidCharts,
        processImages: processImages
    };

    // 自动初始化（如果依赖已就绪）
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 100);
    }

})();
