/**
 * Markdown 渲染器模块
 * 封装 marked.js 配置和 highlight.js 代码高亮
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

    // 初始化 marked.js
    function initMarked() {
        if (!isMarkedReady()) {
            console.error('marked.js is not loaded!');
            return false;
        }

        // 配置 marked.js 选项
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
            'div': ['class'], 'span': ['class']
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
        isInitialized = true;
        return true;
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
            // 解析 Markdown
            var html = marked.parse(text);

            // 清理 HTML
            if (doSanitize) {
                html = sanitizeHtml(html);
            }

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
        isReady: function() { return isInitialized; }
    };

    // 自动初始化（如果依赖已就绪）
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 100);
    }

})();
