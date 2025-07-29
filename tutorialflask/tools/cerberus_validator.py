from cerberus import Validator

def schema_validator_cerberus(document, schema):
    result = {"final_document": {}, "errors": {}}
    v = Validator(schema)    
    # VALIDATE
    if v.validate(document):
        # NORMALIZED
        norm_doc = v.normalized(document)
        result["final_document"] = norm_doc
    else:
        result["errors"] = v.errors

    return result