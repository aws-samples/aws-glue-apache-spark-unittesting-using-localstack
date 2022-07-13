#!/bin/bash

# Set base directory to download and setup required items
BASE_SPARK_INSTALLATION_DIR="/Users/${USER}/local_spark_setup"
mkdir -p $BASE_SPARK_INSTALLATION_DIR

# An error exit function
error_exit()
{
  echo "$1" 1>&2
  exit 1
}

# -------------------------------------
# Install required tools using brew
# -------------------------------------

echo "Installing required tools using brew"
brew install direnv pipenv pylint libffi openssl mvn pyenv wget openjdk@8 || error_exit "Cannot brew install required tools!"

# Install Python 3.7.10 for Glue PySpark as AWS Glue 2.0 uses Python 3.7 and Spark 2.4.3
# Reference: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
echo "Installing Python 3.7.10"
if [[ ! -d  /Users/${USER}/.pyenv/versions/3.7.10 ]]
then
  pyenv install 3.7.10 || error_exit "Cannot install Python 3.7.10!"
fi


# Set JAVA Home
JAVA_HOME="$(brew --prefix openjdk@8)"
export JAVA_HOME

# -------------------------------------
# Apache Spark installation
# -------------------------------------

# Download Apache Spark 2.4.3 and uncompress

wget -P $BASE_SPARK_INSTALLATION_DIR https://aws-glue-etl-artifacts.s3.amazonaws.com/glue-1.0/spark-2.4.3-bin-hadoop2.8.tgz || error_exit "Cannot download Apache Spark 2.4.3!"

cd ${BASE_SPARK_INSTALLATION_DIR}
tar -xvzf ${BASE_SPARK_INSTALLATION_DIR}/spark-2.4.3-bin-hadoop2.8.tgz || error_exit "Cannot uncompress spark-2.4.3-bin-hadoop2.8.tgz!"
export SPARK_HOME=${BASE_SPARK_INSTALLATION_DIR}/spark-2.4.3-bin-spark-2.4.3-bin-hadoop2.8


# -------------------------------------
# AWS Glue installation
# -------------------------------------
rm -rf ${BASE_SPARK_INSTALLATION_DIR}/aws-glue-libs
git clone --single-branch --branch glue-1.0 https://github.com/awslabs/aws-glue-libs.git || error_exit "Cannot GIT clone https://github.com/awslabs/aws-glue-libs.git!"
mvn -f ./aws-glue-libs/pom.xml -DoutputDirectory=jarsv1 dependency:copy-dependencies || error_exit "Cannot get dependencies using Maven!"
cp -f ${BASE_SPARK_INSTALLATION_DIR}/aws-glue-libs/jarsv1/* ${BASE_SPARK_INSTALLATION_DIR}/spark-2.4.3-bin-spark-2.4.3-bin-hadoop2.8/jars || error_exit "Cannot copy AWS Glue JARs to Spache Spark installation jar directory!"

cd aws-glue-libs

# Generate the zip archive for glue python modules
rm PyGlue.zip
zip -r PyGlue.zip awsglue

cd -
echo $SPARK_HOME
echo $BASE_SPARK_INSTALLATION_DIR
echo "DONE!!"
