FROM python:3.8-slim

# Setting working directory
WORKDIR /app

# Copying requirements before other files for faster sequential builds
COPY requirements.txt ./

# Installing 3rd party python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copying the source code
COPY . .

# Installing IBRK Python API client
RUN cd src/market_watcher/ib_client && \
    python setup.py bdist_wheel && \
    cd ../../..
RUN pip install src/market_watcher/ib_client/dist/ibapi-9.76.1-py3-none-any.whl


# Installing market_watcher_cli tool 
RUN pip install --editable src/.   

CMD ["bash"]