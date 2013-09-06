# Create your views here.
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage
from blogengine.models import Post, Category
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.contrib.flatpages.models import FlatPage

def getPost(request, postSlug):
	# get specific post
	post = Post.objects.filter(slug=postSlug)

	# Display specific post
	return render_to_response('single.html', { 'posts':post}, context_instance=RequestContext(request))

def getCategory(request, categorySlug, selected_page=1):
	# get specified category
	posts = Post.objects.all().order_by('-pub_date')
	category_posts = []
	for post in posts:
		if post.categories.filter(slug=categorySlug):
			category_posts.append(post)

	# add pagination
	pages = Paginator(category_posts, 5)

	# get the category
	category = Category.objects.filter(slug=categorySlug)[0]

	# get specified page
	try:
		returned_page = pages.page(selected_page)
	except EmptyPage:
		returned_page = pages.page(pages.num_pages)

	# Display all the pages
	return render_to_response('category.html', {'posts': returned_page.object_list, 'page': returned_page, 'category': category})

class PostsFeed(Feed):
	title = "My Django Blog posts"
	link = "feeds/posts/"
	description = "Posts are from My Django Blog"

	def items(self):
		return Post.objects.order_by('-pub_date')[:5]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.text