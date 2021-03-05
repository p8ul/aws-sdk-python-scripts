
 <h3 align="center">Boto3 AWS scripts</h3>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python3
* pipenv

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install packages
   ```sh
   pipenv install
   ```
3. Export os variables
    ```shell script
    export AWS_ACCESS_KEY_ID = YOUR_AWS_ACCESS_KEY_ID
    export AWS_SECRET_ACCESS_KEY = YOUR_AWS_SECRET_ACCESS_KEY
    export BUCKET_NAME = YOUR_BUCKET_NAME
    export AWS_STORAGE_REGION = YOUR_AWS_STORAGE_REGION
    ```



<!-- USAGE EXAMPLES -->
## Usage
Navigate to the `aws_script` directory
    ```
    cd src
    ```

## Download S3 bucket files
Download files from S3 bucket
```python
from aws_script import S3

bucket_search_query='{bucket_name}/{folder_to_such}'

S3.download_file(dir_name=bucket_search_query)

```


## List buckets
```python
from aws_script import S3

from aws_script import S3
S3.buckets()
```


