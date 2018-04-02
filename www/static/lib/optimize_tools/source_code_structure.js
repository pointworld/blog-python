/**
 * source code optimize tool
 * C by Point on 02/28/2018.
 * M by Point on ...
 *
 * 目的：优化 HTML 文档源文本的树结构
 *
 * 目标：让 HTML 文档具有如下树结构
 *    html
 *      > head
 *      > body
 *        > article
 *          > h 系列标签
 *          > p
 *          > pre
 *
 *
 *
 *
 *
 *
 * 实现：
 *  输入：未优化前的 article 元素
 *  输出：已优化后的 article 元素
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 *
 */

let ScsoTool = {}
// get article element
let article_Ele = document.getElementsByTagName('article')[0]
// get all element nodes in article node
let arrAllNodes = article_Ele.getElementsByTagName('*')
// an array container to ship unoptimized target elements
let arrTargetEles = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
// foreach arrAllNodes
for (let i=0,len=arrAllNodes.length; i<len; i++) {
  arrAllNodes[i].style=''
  arrAllNodes[i].className=''
}
