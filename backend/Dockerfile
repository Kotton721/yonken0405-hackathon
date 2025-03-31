FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04
ARG PYVER=3.10.15
# インタラクティブなプロンプトを無効化
ENV DEBIAN_FRONTEND=noninteractive

# タイムゾーンを東京に設定
RUN ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone
# 必要なパッケージを1つずつインストール
RUN apt-get update && apt-get install -y --no-install-recommends git
RUN apt-get install -y --no-install-recommends ca-certificates
RUN apt-get install -y --no-install-recommends libssl-dev
RUN apt-get install -y --no-install-recommends libglib2.0-0
RUN apt-get install -y --no-install-recommends libsm6
RUN apt-get install -y --no-install-recommends libxext6
RUN apt-get install -y --no-install-recommends libxrender-dev
RUN apt-get install -y --no-install-recommends build-essential
RUN apt-get install -y --no-install-recommends libffi-dev
RUN apt-get install -y --no-install-recommends libxml2-dev
RUN apt-get install -y --no-install-recommends libxslt1-dev
RUN apt-get install -y --no-install-recommends zlib1g-dev
RUN apt-get install -y --no-install-recommends libhdf5-serial-dev
RUN apt-get install -y --no-install-recommends libncurses5-dev
RUN apt-get install -y --no-install-recommends bzip2
RUN apt-get install -y --no-install-recommends libreadline-gplv2-dev
RUN apt-get install -y --no-install-recommends libncursesw5-dev
RUN apt-get install -y --no-install-recommends libsqlite3-dev
RUN apt-get install -y --no-install-recommends tk-dev
RUN apt-get install -y --no-install-recommends libgdbm-dev
RUN apt-get install -y --no-install-recommends libbz2-dev
RUN apt-get install -y --no-install-recommends liblzma-dev

RUN apt-get update && apt-get install -y wget

RUN rm -rf /var/lib/apt/lists/*
# python
RUN wget -q "https://www.python.org/ftp/python/${PYVER}/Python-${PYVER}.tar.xz" &&\
    tar xvf Python-${PYVER}.tar.xz && \
    cd Python-${PYVER} &&\
    ./configure --enable-optimizations --without-ensurepip --enable-loadable-sqlite-extensions && \
    make -j 8 &&\
    make install && \
    cd ../ && rm -rf Python-${PYVER} && \
    python3 -V && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python
# pip を Python 3.10.15 で直接インストール（システムの python3-pip を避ける）
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip && \
    ln -sf /usr/local/bin/pip3 /usr/bin/pip && \
    ln -sf /usr/local/bin/pip3 /usr/bin/pip3

# 作業ディレクトリを設定
WORKDIR /app

# 必要な Python ライブラリを requirements.txt からインストール
COPY ../requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

#クラッシュしないnumpyに変更(gradedown)
RUN pip install "numpy<2"
# アプリケーションコードをコンテナにコピー
COPY . /app/

# コンテナがリッスンするポートを公開
EXPOSE 8000

ENV PYTHONPATH=/app

# FastAPI アプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
