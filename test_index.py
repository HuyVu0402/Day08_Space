from pageindex.client import PageIndexClient
import inspect

print(inspect.signature(PageIndexClient.submit_document))
print(inspect.signature(PageIndexClient.submit_query))
print(inspect.signature(PageIndexClient.get_retrieval))