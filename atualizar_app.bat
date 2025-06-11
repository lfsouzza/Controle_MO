@echo off
cd /d "C:\Users\Felipe\Documents\01. Projetos\01. Programação\Controle_MO"
echo Atualizando o repositório Git...

git add .
git commit -m "Atualização automática do app Streamlit"
git push origin main

echo.
echo ✅ App atualizado com sucesso no GitHub!
pause
