# Установка зависимостей с поддержкой AVX2
$env:CMAKE_ARGS = "-DGGML_AVX2=ON -DGGML_FMA=ON -DGGML_F16C=ON -DGGML_OPENMP=ON"
pip install -r requirements.txt
