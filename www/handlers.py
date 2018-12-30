#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'point'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
import markdown2
from aiohttp import web
from coroweb import get, post
from apis import Page, APIValueError, APIResourceNotFoundError
from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

# extend point  =================================================================================
@get('/')
async def index():
    return {
        '__template__': 'index.html',
    }
# end point  =================================================================================

# extend point  =================================================================================
@get('/point')
async def point():
    return {
        '__template__': 'point.html',
    }
# end point  =================================================================================

# extend business  =================================================================================

@get('/business')
async def business():
    return {
        '__template__': 'business.html',
    }
# end business  =================================================================================


# extend job  =================================================================================

@get('/interview')
async def interview():
    return {
        '__template__': 'interview.html',
    }
# end job  =================================================================================


# extend idea  =================================================================================
@get('/idea')
async def idea():
    return {
        '__template__': 'idea.html',
    }

@get('/idea/process')
async def idea_process():
    return {
        '__template__': 'idea_process.html',
    }

@get('/idea/object')
async def idea_object():
    return {
        '__template__': 'idea_object.html',
    }

@get('/idea/modularization')
async def idea_modularization():
    return {
        '__template__': 'idea_modularization.html',
    }

@get('/idea/component')
async def idea_component():
    return {
        '__template__': 'idea_component.html',
    }

@get('/idea/pipe')
async def idea_pipe():
    return {
        '__template__': 'idea_pipe.html',
    }


@get('/seo')
async def seo():
    return {
        '__template__': 'seo.html',
    }

@get('/hack')
async def hack():
    return {
        '__template__': 'hack.html',
    }

# end idea  =================================================================================

# extend others  =================================================================================
@get('/wave')
async def wave():
    return {
        '__template__': 'wave.html',
    }

@get('/futureman')
async def futureman():
    return {
        '__template__': 'futureman.html',
    }

@get('/brain')
async def brain():
    return {
        '__template__': 'brain.html',
    }

@get('/architecture')
async def architecture():
    return {
        '__template__': 'architecture.html',
    }

@get('/tcp')
async def tcp():
    return {
        '__template__': 'tcp.html',
    }

@get('/urn')
async def urn():
    return {
        '__template__': 'urn.html',
    }


# end others  =================================================================================


# extend company  =================================================================================
@get('/shsnc')
async def shsnc():
    return {
        '__template__': 'shsnc.html',
    }

# end company  =================================================================================


# extend computer  =================================================================================
@get('/computer')
async def computer():
    return {
        '__template__': 'computer.html',
    }

@get('/hardware/harddisk')
async def hardware_harddisk():
    return {
        '__template__': 'hardware_harddisk.html',
    }

@get('/hardware/network_adapter')
async def hardware_network_adapter():
    return {
        '__template__': 'hardware_network_adapter.html',
    }

@get('/software_engineering')
async def software_engineering():
    return {
        '__template__': 'software_engineering.html',
    }
# end computer  =================================================================================

# extend code  =================================================================================
@get('/code')
async def code():
    return {
        '__template__': 'code.html',
    }

@get('/code_comment')
async def code_comment():
    return {
        '__template__': 'code_comment.html',
    }
# end code  =================================================================================


# extend network  =================================================================================
@get('/network')
async def network():
    return {
        '__template__': 'network.html',
    }

@get('/network/architecture')
async def network_architecture():
    return {
        '__template__': 'network_architecture.html',
    }

@get('/network/OSI_model')
async def network_osi():
    return {
        '__template__': 'network_osi-model.html',
    }

@get('/network/protocol')
async def network_protocol():
    return {
        '__template__': 'network_protocol.html',
    }

@get('/network/firewall')
async def network_firewall():
    return {
        '__template__': 'network_firewall.html',
    }

@get('/http')
async def http():
    return {
        '__template__': 'http.html',
    }


# end network  =================================================================================

# extend data  =================================================================================
@get('/data')
async def data():
    return {
        '__template__': 'data.html',
    }

@get('/data/structure')
async def data_structure():
    return {
        '__template__': 'data_structure.html',
    }

@get('/thesis')
async def thesis():
    return {
        '__template__': 'thesis.html',
    }

# end data  =================================================================================

# extend math  =================================================================================
@get('/math')
async def math():
    return {
        '__template__': 'math.html',
    }

@get('/math/thought')
async def math_thought():
    return {
        '__template__': 'math_thought.html',
    }


# end math  =================================================================================

# extend algorithm  =================================================================================
@get('/algorithm')
async def algorithm():
    return {
        '__template__': 'algorithm.html',
    }

@get('/algorithm/recursion')
async def algorithm_recursion():
    return {
        '__template__': 'recursion.html',
    }

# end algorithm  =================================================================================

# extend machine  =================================================================================
@get('/machine')
async def machine():
    return {
        '__template__': 'machine.html',
    }

# end machine  =================================================================================

# extend language  =================================================================================
@get('/language')
async def language():
    return {
        '__template__': 'language.html',
    }

@get('/language/machine')
async def language_machine():
    return {
        '__template__': 'language_machine.html',
    }

@get('/language/assembler')
async def language_assembler():
    return {
        '__template__': 'language_assembler.html',
    }

@get('/programming_language')
async def programming_language():
    return {
        '__template__': 'programming_language.html',
    }

@get('/event-driven_programming')
async def event_driven_programming():
    return {
        '__template__': 'event-driven_programming.html',
    }

@get('/object-oriented_programming')
async def object_oriented_programming():
    return {
        '__template__': 'object-oriented_programming.html',
    }
# end language  =================================================================================


# extend os  =================================================================================
@get('/os')
async def os():
    return {
        '__template__': 'os.html',
    }


@get('/os/win10')
async def os_win10():
    return {
        '__template__': 'os_win10.html',
    }

# end os  =================================================================================

# extend front_end  =================================================================================
@get('/frontEnd')
async def frontEnd():
    return {
        '__template__': 'frontEnd.html',
    }

@get('/frontEnd/engineering')
async def frontEnd_engineering():
    return {
        '__template__': 'frontEnd_engineering.html',
    }
# end front_end  =================================================================================


# extend mv*  =================================================================================
@get('/angular')
async def angular():
    return {
        '__template__': 'angular.html',
    }

@get('/react')
async def react():
    return {
        '__template__': 'react.html',
    }

@get('/vue')
async def vue():
    return {
        '__template__': 'vue.html',
    }


# end mv*  =================================================================================


# extend tools  =================================================================================
@get('/tools')
async def tools():
    return {
        '__template__': 'tools.html',
    }

@get('/tools/vcs')
async def tools_vcs():
    return {
        '__template__': 'tools_vcs.html',
    }

@get('/tools/vcs/git')
async def tools_vcs_git():
    return {
        '__template__': 'tools_vcs_git.html',
    }

@get('/tools/git')
async def tools_git():
    return {
        '__template__': 'tools_git.html',
    }

@get('/tools/database/mysql')
async def tools_database_mysql():
    return {
        '__template__': 'tools_database_mysql.html',
    }

@get('/cron')
async def cron():
    return {
        '__template__': 'cron.html',
    }


@get('/topo')
async def topo():
    return {
        '__template__': 'topo.html',
    }

# end tools  =================================================================================

# extend app  =================================================================================
@get('/app')
async def app():
    return {
        '__template__': 'app.html',
    }

@get('/wechat_mini_program')
async def wechat_mini_program():
    return {
        '__template__': 'wechat_mini_program.html',
    }

# 正则表达式
@get('/regexp')
async def regexp():
    return {
        '__template__': 'regexp.html',
    }


# end app  =================================================================================

# extend web  =================================================================================
@get('/web')
async def web():
    return {
        '__template__': 'web.html',
    }

@get('/web/tool')
async def web_tools():
    return {
        '__template__': 'web_tool.html',
    }

@get('/webpack')
async def webpack():
    return {
        '__template__': 'webpack.html',
    }

@get('/cooking')
async def cooking():
    return {
        '__template__': 'cooking.html',
    }

@get('/web/api')
async def api():
    return {
        '__template__': 'web_api.html',
    }

@get('/web/reference')
async def web_reference():
    return {
        '__template__': 'web_reference.html',
    }

@get('/web/building')
async def web_building():
    return {
        '__template__': 'web_building.html',
    }

@get('/web/safe')
async def web_safe():
    return {
        '__template__': 'web_safe.html',
    }

@get('/web/performance')
async def web_performance():
    return {
        '__template__': 'web_performance.html',
    }

@get('/web/interview')
async def web_interview():
    return {
        '__template__': 'web_interview.html',
    }

@get('/web/browser')
async def web_browser():
    return {
        '__template__': 'web_browser.html',
    }

@get('/web/optimization')
async def web_optimization():
    return {
        '__template__': 'web_optimization.html',
    }

@get('/web/safety')
async def web_safety():
    return {
        '__template__': 'web_safety.html',
    }

@get('/web/runenv')
async def web_runenv():
    return {
        '__template__': 'web_runenv.html',
    }

@get('/web/lib')
async def web_lib():
    return {
        '__template__': 'web_lib.html',
    }

# end web  =================================================================================

# extend bom  =================================================================================
@get('/bom')
async def bom():
    return {
        '__template__': 'bom.html',
    }

@get('/bom/window')
async def bom_window():
    return {
        '__template__': 'bom_window.html',
    }

@get('/bom/window/document')
async def bom_window_document():
    return {
        '__template__': 'bom_window_document.html',
    }

@get('/bom/window/event')
async def bom_window_event():
    return {
        '__template__': 'bom_window_event.html',
    }

@get('/js/bom/ajax')
async def js_ajax():
    return {
        '__template__': 'js_ajax.html',
    }

@get('/js/bom/xmlHttpRequest')
async def js_bom_xmlHttpRequest():
    return {
        '__template__': 'xmlHttpRequest.html',
    }

# end bom  =================================================================================

# extend es  =================================================================================
@get('/es')
async def es():
    return {
        '__template__': 'es.html',
    }

@get('/es/spec')
async def es_spec():
    return {
        '__template__': 'es_spec.html',
    }

@get('/es/spec_cn')
async def es_spec_cn():
    return {
        '__template__': 'es_spec_cn.html',
    }


# end es  =================================================================================


# extend js  =================================================================================
@get('/js')
async def js():
    return {
        '__template__': 'js.html',
    }

@get('/js/lib')
async def js_lib():
    return {
        '__template__': 'js_lib.html',
    }

@get('/js/lib/jquery')
async def js_lib_jquery():
    return {
        '__template__': 'js_lib_jquery.html',
    }

@get('/js/web-api/storage')
async def js_web_api_storage():
    return {
        '__template__': 'js_web_api_storage.html',
    }

@get('/js/es')
async def js_es():
    return {
        '__template__': 'js_es.html',
    }

@get('/js/es/func')
async def js_es_func():
    return {
        '__template__': 'js_es_func.html',
    }

@get('/js/es/obj')
async def js_es_obj():
    return {
        '__template__': 'js_es_obj.html',
    }


@get('/js/es/obj_builtin')
async def js_es_obj_builtin():
    return {
        '__template__': 'js_es_obj_builtin.html',
    }

@get('/js/es/obj_builtin_number')
async def js_es_obj_builtin_number():
    return {
        '__template__': 'js_es_obj_builtin_number.html',
    }

@get('/js/es/obj_builtin_array')
async def js_es_obj_builtin_array():
    return {
        '__template__': 'js_es_obj_builtin_array.html',
    }

@get('/js/es/obj_builtin_func')
async def js_es_obj_builtin_func():
    return {
        '__template__': 'js_es_obj_builtin_func.html',
    }

@get('/js/es/obj_builtin_object')
async def js_es_obj_builtin_object():
    return {
        '__template__': 'js_es_obj_builtin_object.html',
    }

@get('/js/es/obj_builtin_regexp')
async def js_es_obj_builtin_regexp():
    return {
        '__template__': 'js_es_obj_builtin_regexp.html',
    }

@get('/js/es/obj_builtin_string')
async def js_es_obj_builtin_string():
    return {
        '__template__': 'js_es_obj_builtin_string.html',
    }

@get('/js/es/obj_builtin_set')
async def js_es_obj_builtin_set():
    return {
        '__template__': 'js_es_obj_builtin_set.html',
    }


@get('/js/es/obj_builtin_map')
async def js_es_obj_builtin_map():
    return {
        '__template__': 'js_es_obj_builtin_map.html',
    }

@get('/js/es/obj_builtin_symbol')
async def js_es_obj_builtin_symbol():
    return {
        '__template__': 'js_es_obj_builtin_symbol.html',
    }


@get('/js/es/obj_builtin_proxy')
async def js_es_obj_builtin_proxy():
    return {
        '__template__': 'js_es_obj_builtin_proxy.html',
    }

@get('/js/es/obj_builtin_reflect')
async def js_es_obj_builtin_reflect():
    return {
        '__template__': 'js_es_obj_builtin_reflect.html',
    }

@get('/js/es/obj_builtin_promise')
async def js_es_obj_builtin_promise():
    return {
        '__template__': 'js_es_obj_builtin_promise.html',
    }

@get('/js/es/obj_builtin_json')
async def js_es_obj_builtin_json():
    return {
        '__template__': 'js_es_obj_builtin_json.html',
    }

@get('/js/es/obj_builtin_iterator')
async def js_es_obj_builtin_iterator():
    return {
        '__template__': 'js_es_obj_builtin_iterator.html',
    }

@get('/js/es/obj_builtin_generator')
async def js_es_obj_builtin_generator():
    return {
        '__template__': 'js_es_obj_builtin_generator.html',
    }


# extend js end  =================================================================================


# extend node  =================================================================================
@get('/node')
async def node():
    return {
        '__template__': 'node.html',
    }

@get('/node/doc')
async def node_doc():
    return {
        '__template__': 'node_doc.html',
    }

@get('/node/crawler')
async def crawlerer():
    return {
        '__template__': 'node_crawler.html',
    }

@get('/node/web')
async def node_web():
    return {
        '__template__': 'node_web.html',
    }


# extend node end  =================================================================================

# extend Python  =================================================================================
@get('/py')
async def py():
    return {
        '__template__': 'py.html',
    }

# python language reference
@get('/py/spec')
async def py_spec():
    return {
        '__template__': 'py_spec.html',
    }

# python language spec statement
@get('/py/spec/statement')
async def py_spec_statement():
    return {
        '__template__': 'py_spec_statement.html',
    }

# python language spec data_model
@get('/py/spec/data_model')
async def py_spec_data_model():
    return {
        '__template__': 'py_spec_data_model.html',
    }

# python language spec import_system
@get('/py/spec/import_system')
async def py_spec_import_system():
    return {
        '__template__': 'py_spec_import_system.html',
    }

# python language spec function
@get('/py/spec/function')
async def py_spec_function():
    return {
        '__template__': 'py_spec_function.html',
    }

# python language spec object
@get('/py/spec/object')
async def py_spec_object():
    return {
        '__template__': 'py_spec_object.html',
    }

# python standard library
@get('/py/stdlib')
async def py_stdlib():
    return {
        '__template__': 'py_stdlib.html',
    }

# python standard library: built-in functions
@get('/py/stdlib/builtin_functions')
async def py_stdlib_builtin_functions():
    return {
        '__template__': 'py_stdlib_builtin_functions.html',
    }

# python standard library: built-in constants
@get('/py/stdlib/builtin_constants')
async def py_stdlib_builtin_constants():
    return {
        '__template__': 'py_stdlib_builtin_constants.html',
    }

# python standard library: built-in types
@get('/py/stdlib/builtin_types')
async def py_stdlib_builtin_types():
    return {
        '__template__': 'py_stdlib_builtin_types.html',
    }

# python standard library: built-in types: numerics
@get('/py/stdlib/builtin_types_numerics')
async def py_stdlib_builtin_types_numerics():
    return {
        '__template__': 'py_stdlib_builtin_types_numerics.html',
    }

# python standard library: built-in types: sequences
@get('/py/stdlib/builtin_types_sequences')
async def py_stdlib_builtin_types_sequences():
    return {
        '__template__': 'py_stdlib_builtin_types_sequences.html',
    }

# python standard library: built-in types: str
@get('/py/stdlib/builtin_types_str')
async def py_stdlib_builtin_types_str():
    return {
        '__template__': 'py_stdlib_builtin_types_str.html',
    }

# python standard library: built-in types: list
@get('/py/stdlib/builtin_types_list')
async def py_stdlib_builtin_types_list():
    return {
        '__template__': 'py_stdlib_builtin_types_list.html',
    }

# python standard library: built-in types: tuple
@get('/py/stdlib/builtin_types_tuple')
async def py_stdlib_builtin_types_tuple():
    return {
        '__template__': 'py_stdlib_builtin_types_tuple.html',
    }

# python standard library: built-in types: set
@get('/py/stdlib/builtin_types_set')
async def py_stdlib_builtin_types_set():
    return {
        '__template__': 'py_stdlib_builtin_types_set.html',
    }

# python standard library: built-in types: dict
@get('/py/stdlib/builtin_types_dict')
async def py_stdlib_builtin_types_dict():
    return {
        '__template__': 'py_stdlib_builtin_types_dict.html',
    }

# python standard library: re
@get('/py/stdlib/re')
async def py_stdlib_re():
    return {
        '__template__': 'py_stdlib_re.html',
    }

# python standard library: json
@get('/py/stdlib/json')
async def py_stdlib_json():
    return {
        '__template__': 'py_stdlib_json.html',
    }

# python standard library: enum
@get('/py/stdlib/enum')
async def py_stdlib_enum():
    return {
        '__template__': 'py_stdlib_enum.html',
    }

# python standard library: enum
@get('/py/stdlib/urllib')
async def py_stdlib_urllib():
    return {
        '__template__': 'py_stdlib_urllib.html',
    }

@get('/py/glossary')
async def py_glossary():
    return {
        '__template__': 'py_glossary.html',
    }

@get('/py/interpreter')
async def py_interpreter():
    return {
        '__template__': 'py_interpreter.html',
    }
# extend end Python  =================================================================================

# extend Python 爬虫  =================================================================================
@get('/python/webspider')
async def python_webspider():
    return {
        '__template__': 'python_webspider.html',
    }
# extend end Python 爬虫  =================================================================================

# extend HTML 文档  =================================================================================
@get('/html')
async def html():
    return {
        '__template__': 'html.html',
    }

@get('/html/tags')
async def html_tags():
    return {
        '__template__': 'html_tags.html',
    }

@get('/html/html5')
async def html_html5():
    return {
        '__template__': 'html_html5.html',
    }

@get('/html/attrs')
async def html_attrs():
    return {
        '__template__': 'html_attrs.html',
    }

@get('/html/tiy')
async def html_tiy():
    return {
        '__template__': 'html_tiy.html',
    }

@get('/canvas')
async def canvas():
    return {
        '__template__': 'canvas.html',
    }

@get('/bigFileUpload')
async def bigFileUpload():
    return {
        '__template__': 'bigFileUpload.html',
    }

# extend end HTML  =================================================================================

# extend word =================================================================================
@get('/word')
async def word():
    return {
        '__template__': 'c-word.html',
    }

@get('/word/catalog')
async def word_catalog():
    return {
        '__template__': 'c-word-catalog.html',
    }

# extend end word  =================================================================================

# extend css 文档  =================================================================================
@get('/css/css3')
async def css_css3():
    return {
        '__template__': 'css_css3.html',
    }

@get('/css/selector')
async def css_selector():
    return {
        '__template__': 'css_selector.html',
    }


@get('/css/style')
async def css_style():
    return {
        '__template__': 'css_style.html',
    }

@get('/css/attr')
async def css_attr():
    return {
        '__template__': 'css_attr.html',
    }


@get('/css/tiy')
async def css_tiy():
    return {
        '__template__': 'css_tiy.html',
    }

# extend end css  =================================================================================

# extend others  =================================================================================
@get('/bootstrap')
async def bootstrap():
    return {
        '__template__': 'bootstrap.html',
    }
# extend end others  =================================================================================



























@get('/blog/{id}') # 日志详情页
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }

@get('/register') # 注册页
def register():
    return {
        '__template__': 'register.html'
    }

@get('/signin') # 登录页
def signin():
    return {
        '__template__': 'signin.html'
    }

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout') # 注销页
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@get('/manage/')
def manage():
    return 'redirect:/manage/comments'

@get('/manage/comments') # 评论列表页
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }

@get('/manage/blogs') # 日志列表页
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }

@get('/manage/blogs/create') # 创建日志页
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }

@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

@get('/manage/users') # 用户列表页
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }

@get('/api/comments') # 获取评论
async def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)

@post('/api/blogs/{id}/comments') # 创建评论
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment

@post('/api/comments/{id}/delete') # 删除评论
async def api_delete_comments(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    await c.remove()
    return dict(id=id)

@get('/api/users') # 获取用户
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users') # 创建新用户
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/api/blogs') # 获取日志
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)

@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog

@post('/api/blogs') # 创建日志
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog

@post('/api/blogs/{id}') # 修改日志
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog

@post('/api/blogs/{id}/delete') # 删除日志
async def api_delete_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    await blog.remove()
    return dict(id=id)
