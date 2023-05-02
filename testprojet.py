from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://test:test@cluster0.pfcsyrs.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Get the database and collection
db = client["LeoSmartAss"]  # Replace "your_database_name" with the actual name of your database
collection = db["Cours"]  # Replace "your_collection_name" with the actual name of your collection
print(collection)
# Call the API and display the output
try:
    # Replace this example query with your desired query
    query = {"Domaine": "value"}  # Replace "field_name" with the actual field name and "value" with the value you want to query
    # Find documents in the collection that match the query
    result = collection.find(query)
    # Display the results
    for document in result:
        print(document)

except Exception as e:
    print("Error querying the API:", e)