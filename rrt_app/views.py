from django.shortcuts import render, redirect, get_object_or_404
from .models import Issue, Component
from .forms import IssueForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

# View for the form to create a new issue

def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        print(request.user)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user # Set the user who is creating the issue
            issue.save()
            return redirect('issue_list')  # Redirect to the page where issues are listed
    else:
        form = IssueForm()

    return render(request, 'rrt_app/create_issue.html', {'form': form})

# View to display the list of issues based on their approval status

def issue_list(request):
    approved_issues = Issue.objects.filter(is_approved=True).order_by('component__name')
    unapproved_issues = Issue.objects.filter(is_approved=False)

    return render(request, 'rrt_app/issue_list.html', {
        'approved_issues': approved_issues,
        'unapproved_issues': unapproved_issues,
    })

# Live data approval status

def view_data(request):
    # Fetch all components and their related issues
    # components = Component.objects.filter(issues__is_approved=True).prefetch_related('issues')                              
    components = Issue.objects.filter(is_approved=True)
    print(components)                        
    # print(components)
    

    return render(request, 'rrt_app/view_data.html', {
        'components': components,
    })

# View to approve an issue

def approve_issue(request, pkt_id):
    issue = get_object_or_404(Issue, pk=pkt_id)
    issue.is_approved = True
    issue.save()
    return redirect('issue_list')

def disapprove_issue(request, pkt_id):
    issue = get_object_or_404(Issue, pk=pkt_id)
    issue.is_approved = False
    issue.save()
    return redirect('issue_list')

# View to delete an issue

def delete_issue(request, pkt_id):
    issue = get_object_or_404(Issue, pk=pkt_id)
    issue.delete()
    return redirect('issue_list')

# View to edit an issue

def edit_issue(request, pkt_id):
    issue = get_object_or_404(Issue, pk=pkt_id)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issue_list')
    else:
        form = IssueForm(instance=issue)
    
    return render(request, 'rrt_app/edit_issue.html', {'form': form, 'issue': issue})



# Dashboard  +++++++++++++++++++++++++++++++++++++++++


def troubleshooting_dashboard(request):
    selected_component = request.GET.get('component')
    selected_issue = request.GET.get('issue')
    search_query = request.GET.get('q')

    components = Component.objects.filter(issues__is_approved=True).distinct()

    # Build nested dict: {Component Name: {Issue Description: Issue Object}}
    data = {}
    for comp in components:
        issues_qs = comp.issues.filter(is_approved=True)
        if search_query:
            issues_qs = issues_qs.filter(
                Q(description__icontains=search_query) |
                Q(error_message__icontains=search_query) |
                Q(troubleshooting__icontains=search_query) |
                Q(action_plan__icontains=search_query)
            )
        issues_dict = {issue.description: issue for issue in issues_qs}
        if issues_dict:
            data[comp.name] = issues_dict

    selected = None
    if selected_component and selected_issue:
        try:
            selected = Issue.objects.get(
                component__name=selected_component,
                description=selected_issue,
                is_approved=True
            )
        except Issue.DoesNotExist:
            selected = None

    context = {
        'data': data,
        'selected_component': selected_component,
        'selected_issue': selected_issue,
        'selected': selected,
        'search_query': search_query
    }
    return render(request, 'rrt_app/dashboard.html', context)


def ajax_issue_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        matches = Issue.objects.filter(
            is_approved=True
        ).filter(
            Q(description__icontains=query) |
            Q(component__name__icontains=query) |
            Q(troubleshooting__icontains=query) |
            Q(action_plan__icontains=query)
        )[:5]

        for issue in matches:
            match_field = 'description'
            snippet = issue.description
            if query.lower() in issue.component.name.lower():
                match_field = 'component'
                snippet = issue.component.name
            elif query.lower() in issue.troubleshooting.lower():
                match_field = 'troubleshooting'
                snippet = issue.troubleshooting[:100] + '...'

            results.append({
                'component': issue.component.name,
                'issue': issue.description,
                'label': issue.description,
                'match_field': match_field,
                'snippet': snippet,
            })

    return JsonResponse(results, safe=False)

# Dashboard  +++++++++++++++++++++++++++++++++++++++++

