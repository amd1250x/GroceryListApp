from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import GroceryListForm, ItemForm, PersonForm, PersonToItemForm
from .calculator import *
import json
from .models import *
import datetime
# Create your views here.

def IndexView(request):
    if request.method == "POST":
        form = GroceryListForm(request.POST)
        if form.is_valid():
            glist = GroceryList(name=form.cleaned_data["name"],
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

def GroceryListDetailView(request, glist_id):
    glist = GroceryList.objects.get(id=glist_id)
    item_list = Item.objects.filter(glist=glist)
    person_list = Person.objects.filter(glist=glist)
    
    return render(request, "glist.html", {
        'glist':glist,
        'item_list':item_list,
        'person_list':person_list
    })

def glists(request):
    if request.method == "POST":
        glist = GroceryList(name=request.body['name'],
                            buyer=request.body["buyer"], 
                            date=datetime.date.today())
        glist.save()
        return JsonResponse()
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
        return JsonResponse(response)
    else:
        return JsonResponse({"error":"Invalid Request Method"})

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

def persons(request, glist_id):
    if request.method == "POST":
        person = Person(name=request.POST['name'],
                        glist=GroceryList.objects.get(id=glist_id))
        person.save()
        return JsonResponse({"success":"Successfully added person to list"})
    elif request.method == "GET":
        persons = Person.objects.all()
        response = {}
        for p in persons:
            response[p.id]['name'] = p.name
            resposne[p.id]['glist'] = p.glist.id
        return JsonResponse(response)
    else:
        return JsonResponse({"error":"Invalid Request Method"})

def person(request, glist_id, person_id):
    if request.method == "PUT":
        pass
    elif request.method == "DELETE":
        person = Person.objects.get(id=person_id)
        person.delete()
        return JsonResponse({"success":"Successfully deleted Person"})
    elif request.method == "PATCH":
        pass
    elif request.method == "GET":
        pass
    else:
        return JsonResponse({"error": "Invalid Request Method"})

def AddPersonToItem(request, glist_id, item_id, person_id):
    item = Item.objects.get(id=item_id)
    glist = GroceryList.objects.get(id=glist_id)
    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        item.people.add(person)
        item.save()
        return JsonResponse({"sucesss":True})
    else:
        return redirect("/glist/" + str(glist_id))

def RemPersonFromItem(request, glist_id, item_id, person_id):
    item = Item.objects.get(id=item_id)
    glist = GroceryList.objects.get(id=glist_id)
    person = Person.objects.get(id=person_id)

    if request.method == "POST":
        item.people.remove(person)
        item.save()
        return JsonResponse({"sucesss":True})
    else:
        return redirect("/glist/" + str(glist_id))

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
            return JsonResponse({'error':"Item doesn't have user"})
        cost_per_person = cost / people
        for p in person_list:
            if p in i.people.all():
                p.cost += float(cost_per_person)
            p.save()

    response = {}
    for p in person_list:
        response[p.id] = p.cost

    return JsonResponse(response)


    
