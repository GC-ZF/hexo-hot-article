@echo off
echo ��Ҫ�ύ���ļ�
git status
set /p t2="�ύ��Ϣ��"
git add .
git commit -m "%t2%"
git push
pause