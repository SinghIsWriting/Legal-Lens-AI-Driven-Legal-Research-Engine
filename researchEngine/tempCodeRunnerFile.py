for n, hits in enumerate(results):
    for hit in hits:
        print("--------------------------------")
        print(hit)
        print("Type of hit:", type(hit))
        print("Attributes of hit:", dir(hit))
        print("--------------------------------")