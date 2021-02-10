# Akita HTTP Archive (HAR) Utility

This package provides Pydantic models for HTTP Archive (HAR) files, along with
a thread-safe file-writer for creating and concurrently writing HAR entries.

## See it in Action

Take a look at the [Akita Django
Integration](https://github.com/akitasoftware/akita-django), which extends the
`django.test.Client` to produce a HAR file containing requests and responses
from Django integration tests.
