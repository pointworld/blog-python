/**
 * code editor
 * 描述：在浏览器文档可编辑模式下实现代码内容的样式和排版
 *      即在浏览器中实现类似一般代码编辑器的部分功能
 *
 * 实现：
 *   0. 参考已有的并且常用的文本编辑器来实现，如 atom、sublime、webstorm
 *   1. 获取当前正在被编辑的 pre 或 code 元素
 *   2. 监听在 pre 或 code 元素内的输入事件
 *   3. 当代码发生变化时，代码的样式也相应发生变化
 *
 *
 */

let currentCodeElement = document.getElementByTagname('code')

function operateFunction () {}

currentCodeElement.addEventListener('input', operateFunction, true)
