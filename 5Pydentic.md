# Structured Output in LangChain

 ## 1\. What is Structured Output?

 **Structured output** means asking an LLM to return its response in a predefined format instead of returning plain text.

 ### Normal LLM output

```
Inception is a 2010 science-fiction movie directed by Christopher Nolan.
It has a rating of 8.8/10.
```

 ### Structured output

```
{
    "title": "Inception",
    "year": 2010,
    "director": "Christopher Nolan",
    "rating": 8.8
}
```

 The second format is easier for a program to process.

---

 ## 2\. Why Do We Need Structured Output?

 LLMs normally return **free-form text**. This can make it difficult for applications to reliably extract information.

 Structured output helps us:

 - Get predictable responses
- Easily process LLM responses in Python
- Validate the returned data
- Store data in databases
- Build APIs
- Pass LLM output to other applications
- Work with nested/complex data
- Reduce parsing problems

 ### Example

 Suppose we ask:

```
Tell me about the movie Inception.
```

 We may want:

```
{
    "title": "Inception",
    "year": 2010,
    "director": "Christopher Nolan",
    "rating": 8.8
}
```

 Instead of trying to extract these values manually from a paragraph, we can define a schema and ask the LLM to follow it.

---

 # 3\. Pydantic

 **Pydantic** is a Python library used for defining and validating structured data.

 It provides features such as:

 - Field validation
- Field descriptions
- Type checking
- Nested structures
- Default values
- Required fields
- Data serialization

 Pydantic provides a rich feature set for defining structured data.

---

 # 4\. Basic Pydantic Example

```
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year the movie was released")
    director: str = Field(description="Director of the movie")
    rating: float = Field(description="Movie rating out of 10")
```

 Here we have defined the expected structure of a movie.

 ### Schema

```
Movie
├── title     → str
├── year      → int
├── director  → str
└── rating    → float
```

---

 # 5\. Using Pydantic with LangChain

 We can use `with_structured_output()` to tell LangChain what structure we want from the LLM.

```
import os

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = init_chat_model("groq:qwen/qwen3-32b")

class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year the movie was released")
    director: str = Field(description="Director of the movie")
    rating: float = Field(description="Movie rating out of 10")

model_with_structured = model.with_structured_output(Movie)

response = model_with_structured.invoke(
    "Tell me about the movie Inception"
)

print(response)
```

 ### Example output

```
Movie(
    title="Inception",
    year=2010,
    director="Christopher Nolan",
    rating=8.8
)
```

 Instead of getting a normal text response, we get a **Pydantic object**.

---

 # 6\. `Field()` in Pydantic

 `Field()` allows us to provide additional information about a field.

```
class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year the movie was released")
```

 The descriptions help communicate the intended meaning of the fields to the structured-output system.

 We can also make fields required explicitly:

```
class Movie(BaseModel):
    title: str = Field(..., description="Title of the movie")
    year: int = Field(..., description="Year the movie was released")
```

 `...` means the field is required.

---

 # 7\. `include_raw=True`

 By default:

```
model.with_structured_output(Movie)
```

 returns the parsed structured object.

 If we use:

```
model.with_structured_output(
    Movie,
    include_raw=True
)
```

 LangChain can return information about both the original model message and the parsed result.

 Example:

```
model_with_structured = model.with_structured_output(
    Movie,
    include_raw=True
)

response = model_with_structured.invoke(
    "Tell me about the movie Inception"
)

print(response)
```

 Conceptually, the result contains:

```
{
    "raw": ...,
    "parsed": Movie(...),
    "parsing_error": None
}
```

 This is useful when we want to inspect the original response as well as the parsed structured data.

---

 # 8\. Nested Structures

 Structured output can also contain nested objects.

 For example, a movie can have multiple actors.

 First define an `Actor` model:

```
class Actor(BaseModel):
    name: str
```

 Then use it inside another model:

```
class MovieDetails(BaseModel):
    title: str
    cast: list[Actor]
```

 Now the structure looks like:

```
MovieDetails
│
├── title → str
│
└── cast → list
           │
           ├── Actor
           ├── Actor
           └── Actor
```

 Example output:

```
MovieDetails(
    title="Inception",
    cast=[
        Actor(name="Leonardo DiCaprio"),
        Actor(name="Joseph Gordon-Levitt"),
        Actor(name="Tom Hardy")
    ]
)
```

 This is one of the advantages of Pydantic: it can represent complex and nested data structures.

---

 # 9\. TypedDict

 `TypedDict` is another way to describe the expected structure of dictionary data.

 It comes from Python's typing system.

 Example:

```
from typing_extensions import TypedDict, Annotated

class MovieDict(TypedDict):
    title: Annotated[str, "Title of the movie"]
    year: Annotated[int, "Year the movie was released"]
```

 Then:

```
model_with_structured = model.with_structured_output(MovieDict)

response = model_with_structured.invoke(
    "Tell me about the movie Inception"
)

print(response)
```

 Example result:

```
{
    "title": "Inception",
    "year": 2010
}
```

---

 # 10\. Pydantic vs TypedDict

 Both can be used to describe structured data, but they have different purposes.

 | Feature | Pydantic `BaseModel` | `TypedDict` |
| --- | --- | --- |
| Defines structure | ✅ | ✅ |
| Type hints | ✅ | ✅ |
| Runtime validation | ✅ | ❌ |
| Field descriptions | ✅ | ✅ with `Annotated` |
| Nested structures | ✅ | ✅ |
| Converts/validates data | ✅ | ❌ |
| Rich validation features | ✅ | ❌ |
| Lightweight | Less | More |
| Python built-in typing concept | ❌ | ✅ |

---

 # 11\. When to Use Pydantic?

 Use **Pydantic** when you need:

 - Runtime validation
- Complex schemas
- Nested objects
- Field constraints
- Data conversion/validation
- Reliable structured data
- Strong validation for application logic

 Example:

```
class User(BaseModel):
    name: str
    age: int
```

 Pydantic can validate that the data matches the expected model.

 For more complex applications, Pydantic is usually useful because it provides much more than just type hints.

---

 # 12\. When to Use TypedDict?

 Use **TypedDict** when:

 - You mainly need type information for dictionaries
- You want a lightweight structure
- Runtime validation isn't required
- You want to use Python's typing system
- The data structure is relatively simple

 Think of it as:

```
TypedDict
    ↓
"This dictionary should have these keys and types."
```

 While:

```
Pydantic BaseModel
    ↓
"This data should have this structure AND
I want runtime validation/features."
```

---

 # 13\. Simple Difference

 ### TypedDict

```
class MovieDict(TypedDict):
    title: str
    year: int
```

 Main purpose:

 > **Describe the expected type/shape of a dictionary.**

 ### Pydantic

```
class Movie(BaseModel):
    title: str
    year: int
```

 Main purpose:

 > **Define, parse, and validate structured data at runtime.**

---

 # 14\. Dataclasses

 A **dataclass** is a Python feature that makes it easier to create classes mainly used for storing data.

 Without a dataclass:

```
class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year
```

 With a dataclass:

```
from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: int
```

 Python automatically provides common methods such as an initializer.

 We can create an object:

```
movie = Movie(
    title="Inception",
    year=2010
)
```

---

 # 15\. Dataclass vs Pydantic

 | Feature | Dataclass | Pydantic |
| --- | --- | --- |
| Store data | ✅ | ✅ |
| Type hints | ✅ | ✅ |
| Automatic `__init__` | ✅ | ✅ |
| Runtime validation | Basic/No | ✅ |
| Field descriptions | Limited | ✅ |
| Data parsing/conversion | Limited | ✅ |
| Complex validation | ❌ | ✅ |
| Best for LLM structured output | Sometimes | Often useful |

### Simple idea

```
Dataclass
    ↓
Mainly used to organize/store data

TypedDict
    ↓
Describe the shape of a dictionary

Pydantic
    ↓
Define + parse + validate structured data
```

---

 # 16\. Quick Comparison

```
                    Structured Data
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
      TypedDict       Dataclass        Pydantic
          │               │               │
      Type/shape       Store data      Validation
      of dicts         in classes       + parsing
```

---

 # 17\. Important LangChain Method

 The main method to remember is:

```
model.with_structured_output(Schema)
```

 Example:

```
model_with_structured = model.with_structured_output(Movie)
```

 Then:

```
response = model_with_structured.invoke(
    "Tell me about Inception"
)
```

 The LLM response is returned according to the schema.

---

 # 18\. Key Takeaways

 - **Structured output** makes LLM responses predictable and machine-readable.
- **Pydantic** is useful when we need validation and rich schema definitions.
- **TypedDict** is lightweight and mainly describes the expected shape of dictionaries.
- **Dataclasses** are useful for creating simple data-holding classes.
- `Field()` allows us to add descriptions and validation-related metadata.
- Pydantic supports **nested structures**.
- LangChain provides:

```
model.with_structured_output(...)
```

 to make LLM responses follow a defined schema.

 ### Remember

```
LLM
 ↓
Structured Output
 ↓
Schema
 ↓
Pydantic / TypedDict / Dataclass
 ↓
Reliable data for your application
```
