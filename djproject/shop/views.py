from urllib import response
from . models import *
from . serializers import *
from django.shortcuts import render
from rest_framework import mixins, viewsets, views
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
# Create your views here.


class ProductView (mixins.RetrieveModelMixin, generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    # def get(self, request,pk):
    #     return self.retrieve(request, pk)


class CategoryView(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.get(id=pk)
        serializer = CategorySerializer(queryset)
        serializer_data = serializer.data
        alldata = []
        category_products = Product.objects.filter(
            category_id=serializer_data['id'])
        category_products_serializer = ProductSerializer(
            category_products, many=True)
        serializer_data['category_products'] = category_products_serializer.data
        alldata.append(serializer_data)
        return Response(alldata)


class Profileview(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            queryset = Profile.objects.get(prouser=request.user)
            serializer = ProfileSerializer(queryset)
            response_msg = {"error": False, "data": serializer.data}
        except:
            response_msg = {"error": True, "message": "Something wrong !"}
        return Response(response_msg)


class UserdataUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            user_obj = User.objects.get(username=user)
            user_obj.first_name = data["first_name"]
            user_obj.last_name = data["last_name"]
            user_obj.email = data["email"]
            user_obj.save()
            response_msg = {"error": False, "message": "user is geted"}
        except:
            response_msg = {"error": True, "message": "Something wrong !"}
        return Response(response_msg)


class Profileimageupdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def post(self, request):
        try:
            user=request.user
            query =Profile.objects.get(prouser=user)
            data=request.data 
            serializers=ProfileSerializer(query,data=data,context={"request":request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            response_msg = {"error": False}
        except:
            response_msg = {"error": True,"message":"try again"}
        return Response(response_msg)        

class Mycart(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def list(self, request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers =CartSerializer(query,many=True)
        alldata=[]
        for cart in serializers.data:
            cart_product = CartProduct.objects.filter(cart=cart['id'])
            cart_product_serializer = CartProductSerializer(cart_product,many=True)
            cart["cartproduct"]=cart_product_serializer.data
            alldata.append(cart)
        return Response(alldata)      

class Oldorders(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def list(self, request):
        query = Order.objects.filter(cart__customer=request.user.profile) 
        serializer=OrderSerializer(query,many=True)
        all_data=[]
        for order in serializer.data:
            cart_product=CartProduct.objects.filter(cart_id=order['cart']['id'])
            cart_product_serializer=CartProductSerializer(cart_product,many=True)
            order['cartproduct']=cart_product_serializer.data
            all_data.append(order)  
        return Response(all_data)
    def retrieve(self, request,pk=None):
        query=Order.objects.get(id=pk)
        serializer=OrderSerializer(query)
        data=serializer.data
        all_data=[]
        cart_product= CartProduct.objects.filter(cart_id=data['cart']['id'])
        cartproduct_serializer=CartProductSerializer(cart_product,many=True)
        data['cartproduct']=cartproduct_serializer.data
        all_data.append(data)
        return Response(all_data)
    def create(self, request):
        try:
            data=request.data
            cart_id=data['cart_id']
            address=data['address']
            email=data['email']
            cartobj=Cart.objects.get(id=cart_id)
            cartobj.complete_status=True
            cartobj.save()
            Order.objects.create(
                cart=cartobj,
                address=address,
                email=email,
                total=cartobj.total      
            )
            response_msg = {"error": False}
        except:
            response_msg = {"error": True, "message": "something wroing"}
        return Response(response_msg)        


        
class AddtoCart(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def post(self, request):
        product_id=request.data['id']
        product_object=Product.objects.get(id=product_id)
        cart_cart=Cart.objects.filter(customer=request.user.profile).filter(complete_status=False).first()
        cart_product_object=CartProduct.objects.filter(product__id=product_id).first()
        try:
            if cart_cart:
                this_product_in_cart=cart_cart.cartproduct_set.filter(product=product_object)
                if this_product_in_cart.exists():
                    cart_product_uct=CartProduct.objects.filter(product=product_object).filter(cart__complete_status=False).first() 
                    cart_product_uct.quantity +=1
                    cart_product_uct.subtotal +=product_object.selling_price
                    cart_product_uct.save()
                    cart_cart.total+=product_object.selling_price
                    cart_cart.save()
                else:
                    cart_product_new =CartProduct.objects.create(
                        cart=cart_cart,
                        price=product_object.selling_price,
                        quantity=1,
                        subtotal=product_object.selling_price
                    )    
                    cart_product_new.product.add(product_object) 
                    cart_cart.total+=product_object.selling_price
                    cart_cart.save()
            else:
                Cart.objects.create(customer=request.user.profile,total=0)
                new_cart = Cart.objects.filter(customer=request.user.profile).filter(complete_status=False).first()
                cart_product_new =CartProduct.objects.create(
                        cart=new_cart,
                        price=product_object.selling_price,
                        quantity=1,
                        subtotal=product_object.selling_price
                    )
                cart_product_new.product.add(product_object)
                new_cart.total+=product_object.selling_price
                new_cart.save()
            response_msg = {"error": False}
             
        except:
            response_msg = {"error": True, "message": "try again"}
        return Response(response_msg)    

class Editcart(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def post(self, request):
        cart_product_id=request.data["id"]
        cart_product=CartProduct.objects.get(id=cart_product_id)
        cart_object=cart_product.cart

        cart_product.quantity -=1
        cart_product.subtotal -= cart_product.price
        cart_product.save()

        cart_object.total -= cart_product.price
        cart_object.save()
        print("naim")
        return Response({"message":"cart added"})
       


class Deletecart(views.APIView):
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes=[IsAuthenticated,]
    def post(self, request):
        cart_product=CartProduct.objects.get(id=request.data["id"])
        cart_product.delete()
        return Response({"message":"cart deleted"})

class Deletefullcart(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes=[IsAuthenticated,]
    def post(self, request):
        try:
            cart_id = request.data["id"]
            cart_object =Cart.objects.get(id=cart_id)
            cart_object.delete()
            response = {"error":False,"message":"cart deleted"}
        except:
            response = {"error":True,"message":"no"}
        return Response(response)        


class RegisterApiView(views.APIView):
    def post(self, request):
        serializers=UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error":False,"message":"Registered succesfully","dataset":serializers.data})
        return Response({"error":True,"message":"A user with that name already exixts"})

# class RegisterApiView(views.APIView):
#     def post(self, request):
#         serializers=UserSerializer(data=request.data)
#         if serializers.email.is_exists():
#             return Response({"error":True,"message":"email exixs "}) 
#         else:    
#             serializers.is_valid()
#             serializers.save()
#             return Response({"error":False,"message":"Registered succesfully","dataset":serializers.data})
        