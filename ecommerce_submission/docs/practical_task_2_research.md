# Practical Task 2 — Independent Technical Research

## 1. Python `requests` module

The `requests` package is a Python library that makes it easier for a program to communicate with a web server over HTTP. Instead of manually building a request and parsing a low-level response, a developer can call a function such as `requests.get()` or `requests.post()`. The server's response is represented by a response object, which includes the status code, headers, body and other information. If the server returns JSON, `response.json()` can convert that response body into normal Python data structures.

For example:

```python
import requests

response = requests.get(
    "https://httpbin.org/get",
    params={"category": "books"},
    timeout=10,
)
response.raise_for_status()  # raises an exception for HTTP error status codes
print(response.status_code)
print(response.json())
```

The `params` argument adds query-string parameters to the URL. Other common functions are `requests.post()` for sending data, `requests.put()` or `requests.patch()` for updates, and `requests.delete()` for deletion. A developer can send JSON using `json=...`, form data using `data=...`, and authentication information using supported authentication options. A timeout is important because otherwise a program might wait too long for an unresponsive server. The package must be installed separately with `python -m pip install requests`.

Typical uses include calling a REST API, downloading a file, submitting form data, or checking information exposed by another web service. It should be used with HTTPS for sensitive data, and code should handle connection errors, timeouts, unexpected status codes and untrusted response data.

## 2. JSON and XML data formats

### JSON

JSON (JavaScript Object Notation) is a text format for representing structured data using objects, arrays, strings, numbers, booleans and `null`. Although its name comes from JavaScript, it is used by many programming languages. It is common in web APIs because the structure maps naturally to dictionaries, lists and basic values in Python.

Example:

```json
{
  "product": "Notebook",
  "price": 25.00,
  "available": true,
  "tags": ["stationery", "school"]
}
```

**Advantages of JSON**
1. Its syntax is relatively compact, so messages are often smaller than equivalent XML.
2. It is easy for people to read and write for ordinary data structures.
3. Many languages provide built-in or widely available JSON parsers.
4. Objects and arrays map conveniently to dictionaries and lists in Python and similar structures in other languages.
5. It is widely supported by modern web APIs and JavaScript applications.

**Disadvantages of JSON**
1. The basic format does not define comments, which can make annotated configuration less convenient.
2. It has no native date/time or binary-data type; those values need agreed conventions or encoding.
3. The format itself does not provide a built-in schema or strict validation rules for an application's data model.
4. It does not directly support namespaces, which can matter when combining vocabularies from different XML-based systems.
5. Large or deeply nested documents can still be difficult to inspect and validate without tooling.

### XML

XML (Extensible Markup Language) is a text format that represents data with nested, named elements and attributes. A document has a single root element, and its structure can be described with tools such as XML Schema. XML is used in document exchange, configuration, publishing, and established systems such as some enterprise integrations and SOAP services.

Example:

```xml
<product>
  <name>Notebook</name>
  <price currency="ZAR">25.00</price>
  <available>true</available>
  <tag>stationery</tag>
  <tag>school</tag>
</product>
```

**Advantages of XML**
1. Named opening and closing tags make the structure explicit and can be useful for document-oriented data.
2. XML Schema and related tools can describe and validate the allowed structure and data types.
3. Namespaces help avoid name collisions when different vocabularies are combined.
4. It supports attributes, mixed content and document structures that are useful beyond simple key/value data.
5. It has mature tooling for transformations, queries and document validation.

**Disadvantages of XML**
1. Repeated tags and closing tags often make the same information more verbose than JSON.
2. Documents can be harder to read and hand-write when the structure is deeply nested.
3. Parsing and mapping XML into application objects can require more code than using JSON for simple API payloads.
4. XML parsers must be configured carefully; unsafe external entity processing can introduce security risks.
5. There are multiple related standards and conventions, which can increase implementation complexity.

### Choosing between them

JSON is often a practical default for a straightforward web API that exchanges application data. XML remains useful where a system depends on XML schemas, namespaces, document markup or existing XML-based standards. The best format depends on the systems being integrated, validation needs, document complexity and compatibility requirements.

## 3. RESTful APIs

REST stands for Representational State Transfer. It is an architectural style for designing networked services. A RESTful API exposes resources through URLs and uses standard HTTP methods to work with those resources. For example, an API might use `GET /products/` to list products, `GET /products/12/` to retrieve one product, `POST /products/` to create a product, `PATCH /products/12/` to update part of it, and `DELETE /products/12/` to remove it. The response often contains JSON, but REST does not require JSON specifically.

A well-designed REST interface generally uses a client-server separation, stateless requests, a consistent resource interface, cache controls where appropriate, and representations that describe the resource. Stateless means each request includes the information the server needs to process it rather than relying on hidden conversational state from a previous request. Authentication can still be used; it is simply supplied as part of each request, for example with a token.

RESTful APIs are used to let websites, mobile apps, other services and third-party developers interact with an application's data or capabilities without needing to share the same codebase. An eCommerce API, for example, could expose product listings, store information, carts and order status to different client applications.

**Advantages of RESTful APIs**
1. They use common HTTP methods and status codes, making the interface familiar to many developers.
2. Client and server can be developed separately as long as they agree on the API contract.
3. Stateless requests can make scaling and distributing requests across servers easier.
4. HTTP caching can reduce repeated work and improve performance for suitable responses.
5. Resource-based URLs can provide a clear, consistent way to organise application capabilities.

**Disadvantages of RESTful APIs**
1. Clients may need multiple requests to gather related information, increasing latency for some workflows.
2. A client can receive more fields than it needs, or too little data for a screen, unless the API is designed carefully.
3. The API designer must define consistent resource names, status codes, validation errors, pagination and versioning rules.
4. Stateless requests can require authentication details to be sent repeatedly and do not by themselves preserve a multi-step workflow.
5. Security is not automatic: developers still need authentication, authorization, input validation, rate limiting and HTTPS.

## Short comparison

| Topic | JSON | XML | RESTful API |
|---|---|---|---|
| What it is | A data representation format | A markup-based data representation format | An architectural style for network APIs |
| Main purpose | Exchange structured data | Exchange structured or document-oriented data | Provide network access to resources and operations |
| Common pairing | HTTP APIs and JavaScript clients | Document systems and XML-based standards | HTTP methods with JSON, XML or another representation |
| Main trade-off | Compact and convenient, but limited built-in schema features | Explicit and extensible, but often verbose | Familiar and scalable design pattern, but requires careful API design |

