FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    python3-pip \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pyspark kafka-python cassandra-driver

# Copy scripts and source code
COPY scripts/ /scripts/
COPY src/ /src/
COPY config/ /config/

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Run initialization scripts
RUN /scripts/init-spark.sh
RUN /scripts/init-kafka.sh
RUN /scripts/init-hdfs.sh
RUN /scripts/init-cassandra.sh

# Set the working directory
WORKDIR /src

# Command to run the application
CMD ["python3", "stream_processing.py"]
