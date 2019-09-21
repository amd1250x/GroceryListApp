from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import GroceryListForm, ItemForm, PersonForm, PersonToItemForm
from .calculator import *
import json
from .models import *
import datetime
# Create your views here.


def CalculateRemoval(item):
    for p in item.people.all():
        old_cost_per_person = (item.price * item.quantity) / (len(item.people.all()) or 1)
        print("Old cost: ", old_cost_per_person)
        p.cost -= float(old_cost_per_person)
        p.save()

def CalculateAdditional(item):
    for p in item.people.all():
        new_cost_per_person = (item.price * item.quantity) / (len(item.people.all()) or 1)
        print("New cost: ", new_cost_per_person)
        p.cost += float(new_cost_per_person)
        p.save()


def IndexView(request):
    if request.method == "POST":
        form = GroceryListForm(request.POST)
        if form.is_valid():
            glist = GroceryList(user=request.user,
                                name=form.cleaned_data["name"],
                                buyer=form.cleaned_data["buyer"], 
                                date=datetime.date.today())
            glist.save()

            return render(request, "index.html", {
                'form':form,
                'glists':GroceryList.objects.all()
            })
    else:
        form  = GroceryListForm()


    return render(request, "index.html", {
        'form':form, 
        'glists':GroceryList.objects.all()
    })

@login_required
def GroceryListDetailView(request, glist_id):

    glist = GroceryList.objects.get(id=glist_id)
    item_list = Item.objects.filter(glist=glist)
    person_list = Person.objects.filter(glist=glist)
    
    if request.user == glist.user:
        return render(request, "glist.html", {
            'glist':glist,
            'item_list':item_list,
            'person_list':person_list
        })
    else:
        return IndexView(request)

@login_required
def glists(request):
    if request.method == "POST":
        glist = GroceryList(user=request.user,
                            name=request.POST['name'],
                            buyer=request.POST["buyer"], 
                            date=datetime.date.today())
        glist.save()
        return JsonResponse({"success":"Successfully added List"})
    elif request.method == "GET":
        glists = GroceryList.objects.all()
        response = {}
        for g in glists:
            response[g.id] = {}
            response[g.id]['name'] = g.name
            response[g.id]['buyer'] = g.buyer
            response[g.id]['date'] = g.date
        return JsonResponse(response)
    else:
        return JsonResponse({"error":"Invalid Request Method"})

@login_required
def glist(request, glist_id):
    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        glist = GroceryList.objects.get(id=glist_id)
        glist.delete()
        return JsonResponse({"success":"Successfully deleted List"})
    elif request.method == "PATCH":
        pass
    elif request.method == "GET":
        pass
    else:
        return JsonResponse({"error": "Invalid Request Method"})

@login_required
def items(request, glist_id):
    if request.method == "POST":
        item = Item(name=request.POST['name'], 
                    quantity=request.POST['quantity'],
                    price=request.POST['price'], 
                    glist=GroceryList.objects.get(id=glist_id))
        item.save()
        return JsonResponse({"success": "Successfully added Item"})
    elif request.method == "GET":
        items = Item.objects.filter(glist=GroceryList.objects.get(id=glist_id))
        response = {}
        for i in items:
            response[i.id] = {}
            response[i.id]['name'] = i.name
            response[i.id]['quantity'] = i.quantity
            response[i.id]['price'] = i.price
            response[i.id]['people'] = {}
            for p in i.people.all():
                response[i.id]['people'][p.id] = [p.user.username]
        return JsonResponse(response)
    else:
        return JsonResponse({"error":"Invalid Request Method"})

@login_required
def item(request, glist_id, item_id):
    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        item = Item.objects.get(id=item_id)
        item.delete()
        return JsonResponse({"success":"Successfully deleted Item"})
    elif request.method == "PATCH":
        pass
    elif request.method == "GET":
        pass
    else:
        return JsonResponse({"error": "Invalid Request Method"})

@login_required
def persons(request, glist_id):
    if request.method == "POST":
        person = Person(user=User.objects.get(id=request.POST['user']),
                        glist=GroceryList.objects.get(id=glist_id))
        person.save()
        return JsonResponse({"success":"Successfully added person to list"})
    elif request.method == "GET":
        persons = Person.objects.filter(glist=GroceryList.objects.get(id=glist_id))
        response = {}
        for p in persons:
            response[p.id] = {}
            response[p.id]['name'] = p.user.username
            response[p.id]['cost'] = p.cost
        return JsonResponse(response)
    else:
        return JsonResponse({"error":"Invalid Request Method"})

@login_required
def person(request, glist_id, person_id):
    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        items = Item.objects.all()
        first_pass = False
        for i in items:
            old_cost = (i.price * i.quantity) / (len(i.people.all()) or 1)
            for p in i.people.all():
                p.cost -= float(old_cost)
                p.save()
            if not first_pass:
                person = Person.objects.get(id=person_id)
                person.delete()
                first_pass = True
            new_cost = (i.price * i.quantity) / (len(i.people.all()) or 1)
            for p in i.people.all():
                p.cost += float(new_cost)
                p.save()
        return JsonResponse({"success":"Successfully deleted Person"})
    elif request.method == "PATCH":
        pass
    elif request.method == "GET":
        pass
    else:
        return JsonResponse({"error": "Invalid Request Method"})

@login_required
def AddPersonToItem(request, glist_id, item_id, person_id):
    item = Item.objects.get(id=item_id)
    glist = GroceryList.objects.get(id=glist_id)
    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        CalculateRemoval(item)
        item.people.add(person)
        item.save()
        CalculateAdditional(item)
        return JsonResponse({"sucesss":True})
    else:
        return redirect("/glist/" + str(glist_id))

@login_required
def RemPersonFromItem(request, glist_id, item_id, person_id):
    item = Item.objects.get(id=item_id)
    glist = GroceryList.objects.get(id=glist_id)
    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        CalculateRemoval(item)
        item.people.remove(person)
        item.save()
        CalculateAdditional(item)
        return JsonResponse({"sucesss":True})
    else:
        return redirect("/glist/" + str(glist_id))


@login_required
def CalculateRequest(request, glist_id):
    glist = GroceryList.objects.get(id=glist_id)
    item_list = Item.objects.filter(glist=glist)
    person_list = Person.objects.filter(glist=glist)


    for p in person_list:
        p.cost = 0
        p.save()

    

    for i in item_list:
        cost = i.quantity * i.price
        people = len(i.people.all())
        if people == 0:
            # Prevents div by 0 issue
            people = 1
            #return JsonResponse({'error':"Item doesn't have user"})
        cost_per_person = cost / people

        for p in person_list:
            if i.people.filter(id=p.id):
                p.cost += float(cost_per_person)
                p.save()

    response = {}
    for p in person_list:
        response[p.id] = p.cost

    return JsonResponse(response)

@login_required
def users(request):
    users = User.objects.all()
    
    if request.method == "POST":
        pass
    elif request.method == "GET":
        response = {}
        for u in users:
            response[u.id] = {}
            response[u.id]["name"] = u.username
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "Invalid Request Method"})