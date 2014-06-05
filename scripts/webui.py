#!/usr/bin/env python
#============================================================================
# This file is part of Pwman3.
#
# Pwman3 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2
# as published by the Free Software Foundation;
#
# Pwman3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pwman3; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#============================================================================
# Copyright (C) 2012-2014 Oz Nahum <nahumoz@gmail.com>
#============================================================================
from __future__ import print_function
from bottle import route, run, debug, template, request, redirect
from pwman.util.crypto import CryptoEngine
import pwman.data.factory
from pwman.data.tags import TagNew
from pwman import parser_options, get_conf_options
from pkg_resources import resource_filename

templates_path = [resource_filename('pwman', 'ui/templates')]

AUTHENTICATED = False
TAGS = None
DB = None


@route('/node/:no')
def view_node(no):
    global DB
    node = DB.getnodes([no])
    output = template("view.tpl", node=node[0], template_lookup=templates_path)
    return output


def submit_node(id, request):
    # create new\update node based on request.params.items()
    redirect('/')


@route('/new/', method=['GET', 'POST'])
@route('/edit/:no', method=['GET', 'POST'])
def edit_node(no=None):
    global DB

    if 'POST' in request.method:
        submit_node(no, request)

    if no:
        node = DB.getnodes([no])[0]
    else:

        class Node(object):

            def __init__(self):
                self._id = None
                self.username = ''
                self.password = ''
                self.url = ''
                self.notes = ''
                self.tags = ''

        node = Node()

    output = template('edit.tpl', node=node,
                      template_lookup=templates_path)
    return output


@route('/auth', method=['GET', 'POST'])
def is_authenticated():

    global AUTHENTICATED
    crypto = CryptoEngine.get()

    if request.method == 'POST':
        key = request.POST.get('pwd', '')
        crypto.auth(key)
        AUTHENTICATED = True
        redirect('/')
    else:
        return template("login.tpl", template_lookup=templates_path)


@route('/', method=['GET', 'POST'])
def listnodes():

    global AUTHENTICATED, TAGS, DB

    _filter = None
    OSX = False
    args = parser_options().parse_args()
    xselpath, dbtype = get_conf_options(args, OSX)
    dbver = 0.4
    DB = pwman.data.factory.create(dbtype, dbver)
    DB.open()

    crypto = CryptoEngine.get()

    if not AUTHENTICATED:
        redirect('/auth')

    if 'POST' in request.method:
        _filter = request.POST.get('tag')
        if _filter:
            DB._filtertags = [TagNew(_filter.strip())]
        if _filter == 'None':
            DB._filtertags = []

    nodeids = DB.listnodes()
    nodes = DB.getnodes(nodeids)

    nodesd = [''] * len(nodes)
    for idx, node in enumerate(nodes):
        ntags = [t.strip() for t in filter(None, node.tags)]
        nodesd[idx] = ('@'.join((node.username, node.url)),
                       ', '.join(ntags))

    if not TAGS:
        TAGS = list(set([''.join(node.tags).strip() for node in nodes]))
        TAGS.sort()
        TAGS.insert(0, 'None')

    html_nodes = template("main.tpl", nodes=nodes, tags=TAGS,
                          template_lookup=[resource_filename('pwman',
                                                             'ui/templates')])
    return html_nodes

debug(True)
run(reloader=True)
