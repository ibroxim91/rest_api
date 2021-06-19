class PostCreateView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
# permission_classes = (permissions.IsAdminUser,)


class PostViewSet(viewsets.ViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def get_object(self):
		post = Post.objects.get(pk=self.kwargs['pk'])
		return post

	def delete(self, request, pk=None):
		instance = self.get_object()
		instance.delete()
		return Response({'status': 200})

	def create(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			Post.objects.create(**serializer.validated_data)
			return Response(
				serializer.validated_data, status=status.HTTP_201_CREATED
			)

		return Response({
			'status': 'Bad request',
			'message': 'Account could not be created with received data.'
		}, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk):
		# get the object itself
		instance = self.get_object()
		# modify fields during the update
		serializer = self.serializer_class(instance, data=request.data, partial=False)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response({'status': 200})

	def list(self, request):
		posts = Post.objects.all()
		serializer = self.serializer_class(posts, many=True)
		return Response(serializer.data)