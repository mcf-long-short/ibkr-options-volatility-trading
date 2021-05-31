FROM python:3.8-slim

# Creating non-root user
RUN useradd --create-home --shell /bin/bash app_user

# Setting working directory
WORKDIR /home/app_user

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

# Changing user to the new one
USER app_user

CMD ["bash"]