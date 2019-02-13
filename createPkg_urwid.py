#!/usr/bin/python3


import urwid

choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()


def start():
    body = [urwid.Text(u'EMP Package Wizard'), urwid.Divider()]

    button = urwid.Button('Start')
    urwid.connect_signal(button, 'click', menu)
    body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    body.append( urwid.Divider() )
    body.append( exit_button() )
    
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))



def menu(button):
    choices = [ u'add pkg', u'add component' ]

    pile = [urwid.Text('Menu'), urwid.Divider()]

    b_pkg = urwid.Button( u'add package' )
    urwid.connect_signal( b_pkg, 'click', add_pkg )
    pile.append( urwid.AttrMap(b_pkg, None, focus_map='reversed'))

    b_cmp = urwid.Button( u'add component' )
    urwid.connect_signal( b_cmp, 'click', add_component )
    pile.append( urwid.AttrMap(b_cmp, None, focus_map='reversed'))
    
    pile.append( urwid.Divider() )
    pile.append( exit_button()  )

    main.original_widget = urwid.Filler( urwid.Pile( pile ) )

    
def add_pkg(button) :
    pile = [ urwid.Text('Add Package'), urwid.Divider() ]

    pile.append( exit_button()  )
    main.original_widget = urwid.Filler( urwid.Pile( pile ) )
    
    
def add_component(button) :
    pile = [ urwid.Text('Add Component'), urwid.Divider() ]
    box = urwid.AttrWrap( urwid.CheckBox('Is top'),'buttn','buttnf' )
    pile.append( box )
    pile.append( urwid.Divider() )
    pile.append( exit_button()  )
    main.original_widget = urwid.Filler( urwid.Pile( pile ) )

    
def exit_button():
    done = urwid.Button(u'Exit')
    urwid.connect_signal(done, 'click', exit_program)
    return urwid.AttrMap(done, None, focus_map='reversed')


def exit_program(button):
    raise urwid.ExitMainLoop()


main = urwid.Padding(start(), left=2, right=2)


top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 95),
    valign='middle', height=('relative', 95),
                    min_width=50, min_height=10)

urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

