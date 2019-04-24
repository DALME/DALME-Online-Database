from dalme_app import functions

def dalme_general(request):
    context = {}
    breadcrumb = [('Project', ''), ('Task Lists', '/tasks')]
    sidebar_toggle = request.session['sidebar_toggle']
    context['sidebar_toggle'] = sidebar_toggle
    state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
    context = functions.set_menus(request, context, state)
    page_title = 'Task Lists'
    context['page_title'] = page_title
    context['page_chain'] = functions.get_page_chain(breadcrumb, page_title)
    return context
