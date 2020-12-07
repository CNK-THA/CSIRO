
from fhir.resources.codesystem import CodeSystem

data = {"status":"THIS IS A TEST", "content":"another test"}

code = CodeSystem(data)
print(code.content)
print(code.as_json())

from fhir.resources.backboneelement import BackboneElement

