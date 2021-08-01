from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.views import View


# Create your views here.
def index(request):
    products =None
    categories = Category.get_all_categories()
    categoryID=request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data={}
    data['products']= products
    data['categories'] = categories
    #return render(request,'orders/order.html')
    return render(request,'index.html',data)

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(First_name=first_name,
                            Last_name=last_name,
                            Phone_number=phone,
                            Email=email,
                            Password=password)

        error_message = self.validateCustomer(customer)
        # saving
        if (not error_message):
            print(first_name, last_name, phone, email, password)
            customer.Password = make_password(customer.Password)

            customer.register()

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self,customer):
        error_message = None
        if (not customer.First_name):
            error_message = "first name required !!"
        elif len(customer.First_name) < 4:
            error_message = "first name should have more than 4 character"

        elif (not customer.Last_name):
            error_message = "last name required !!"
        elif len(customer.Last_name) < 4:
            error_message = "last name should have more than 4 character"

        elif (not customer.Phone_number):
            error_message = "phone nnumber required !!"
        elif len(customer.Phone_number) < 10:
            error_message = "phone number should have more than 10 character"

        elif (not customer.Password):
            error_message = "password required !!"
        elif len(customer.Password) < 6:
            error_message = "password should have more than 6 character"
        if (not customer.Email):
            error_message = "email required !!"
        elif len(customer.Email) < 5:
            error_message = "email should have more than 5 character"

        elif customer.isExists():
            error_message = 'Email Address already registered'

        return error_message


class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.Password)
            if flag:
                return redirect('homepage')
            else:
                error_message = 'Email or Password invalid'
        else:
            error_message = 'Email or Password invalid'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})

#def login(request):
    #if request.method == 'GET':

    #else:
