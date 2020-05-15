psycopg2 Python Library for AWS Lambda
===

Issue
---
```
Psycopg is a C wrapper to the libpq PostgreSQL client library.
So to install/use it we need libpq header files,
pg_config program which are usually installed in libpq-dev.
```

When using **psycopg/psycopg2-binary** on AWS Lambda, unlike installing on local, it's necessary to compile related libraries first, and then put the result into the zip file and upload together. The libraries has been installed into `/usr/lib/x86_64-linux-gnu/` when pip installed module on local.


Attempt
---
Although its version is also Python3.6, the Postgres' version is `9.4.3`.

- Error will appear if follow `HOW TO USE` directly
```
Unable to import module 'app/handler': libpq.so.5: cannot open shared object file: No such file or directory
```

- Error will appear if compress all `.so` files and upload to Lambda directly
```
Unable to import module 'app/handler': /lib64/libc.so.6: version `GLIBC_2.25' not found (required by /var/task/libcrypto.so.1.1)
```

- Error will appear if follow the tutorial on repo on OSX to compile manually
```
No module named 'psycopg2._psycopg'
```
According to the [article](https://github.com/jkehler/awslambda-psycopg2/issues/47#issuecomment-532072122), different OS will not compile the same `.so` file. This is why the error above would appear.

|   OS   | macOS | Linux |
| ------ | ----- | ----- |
| **CompiledFile** | **`_psycopg.cpython-36m-darwin.so`** | **`_psycopg.cpython-36m-x86_64-linux-gnu.so`** |



Instructions on compiling this package from scratch (on Linux)
---
Currently Postgres version of Shoplytics is **`9.6.11`**, please use the released date to look for the earliest `psycopg` version if you were to compile the content.

- [PostgreSQL9.6.11](https://www.postgresql.org/ftp/source/v9.6.11/)： `2018-11-05 22:02:03`
- [Psycopg 2.8 released](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/)： `2019-04-04`


```#BASH
<!-- Turn on ubuntu(Linux) -->
docker run -it -d --name ubuntu16.04 ubuntu:16.04

<!-- Enter Bash -->
docker exec -it ubuntu16.04 bash

<!-- Copy directory into project -->
docker cp ubuntu16.04:/psycopg2-2.8/build/lib.linux-x86_64-3.6/psycopg2/_psycopg.cpython-36m-x86_64-linux-gnu.so .
```

```#BASH
# Install python3.6
apt-get install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt-get update && apt-get install python3.6 curl -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py

# Install GCC
apt-get install build-essential -y

# Download files
curl -O https://ftp.postgresql.org/pub/source/v9.6.11/postgresql-9.6.11.tar.gz
# The file from `https://pypi.org/packages/source/p/psycopg2/psycopg2-2.8.tar.gz` is a HTML document text, ASCII text
# And the resource has been moved to https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-2.8.tar.gz
curl -L https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-2.8.tar.gz > psycopg2-2.8.tar.gz

# Unzip files
tar zxvf postgresql-9.6.11.tar.gz
tar zxvf psycopg2-2.8.tar.gz

# Configure the source tree for your system and choose the options in PostgreSQL source directory
postgresql-9.6.11/configure --prefix /postgresql-9.6.11 --without-readline --without-zlib
make
make install

# Edit the setup.cfg file and build in the psycopg2 source directory
apt-get install python3.6-dev -y
sed -i 's/pg_config = /pg_config = \/postgresql-9.6.11\/bin\/pg_config/g' /psycopg2-2.8/setup.cfg
sed -i 's/static_libpq = 0/static_libpq = 1/g' /psycopg2-2.8/setup.cfg
python3.6 setup.py build
```


Instructions on compiling this package from scratch (on OSX)
---
1. Download the [PostgreSQL source code](https://ftp.postgresql.org/pub/source/v9.6.11/postgresql-9.6.11.tar.gz) and extract into a directory.
2. Download the [psycopg2 source code](https://ftp.postgresql.org/pub/source/v9.6.11/postgresql-9.6.11.tar.gz) and extract into a directory.
3. Go into the PostgreSQL source directory and execute the following commands:
    - ./configure --prefix {path_to_postgresql_source} --without-readline --without-zlib
    - make
    - make install
4. Go into the psycopg2 source directory and edit the setup.cfg file with the following:
    - pg_config = {path_to_postgresql_source/bin/pg_config}
    - static_libpq = 1
5. Execute python setup.py build in the psycopg2 source directory.

After the above steps have been completed you will then have a build directory and the custom compiled psycopg2 library will be contained within it. Copy this directory into your AWS Lambda package and you will now be able to access PostgreSQL from within AWS Lambda using the psycopg2 library!


```
Troubleshooting:
    ErrorMessage.1:
        ld: library not found for -lssl
        clang: error: linker command failed with exit code 1 (use -v to see invocation)
        error: command 'gcc' failed with exit status 1
    Try.1:
        env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" python3 setup.py build
```


Ref.
---
- [awslambda-psycopg2](https://github.com/jkehler/awslambda-psycopg2)
- [ErrorCompressedMessage - gzip: stdin: not in gzip format](https://kknews.cc/code/62nbjkv.html)
- [gzip: stdin: not in gzip format](https://askubuntu.com/questions/877292/gzip-stdin-not-in-gzip-format)
- [Aws Lambda Primer With Ruby using the RedShift, Secrets Manager and S3](https://nisdom.com/posts/2019-05-14-aws-lambda-primer-with-ruby-redshift-s3/)

