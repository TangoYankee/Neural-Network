import hello_world

item = {
    'title': 'first',
    'link': 'here.com',
    'location': 'here',
    'original_price': '10',
    'price': '9'
}

testPipeline = hello_world.LivingSocialPipeline()
saved_item  = testPipeline.process_item(item)
print(saved_item)
