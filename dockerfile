FROM python:3.8.10
MAINTAINER zhsher
EXPOSE 8000
WORKDIR /home/hexo-hot-article/
ADD . /home/hexo-hot-article/
ENV TimeZone=Asia/Shanghai
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "api/index.py"]