import hello_world

item = {
    'values': [0.098, 0.872762, 0.12, 0.563]
}

testPipeline = hello_world.BasePipeline()
saved_item = testPipeline.process_cancer(item)
testPipeline.query_database()
