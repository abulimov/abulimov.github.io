This is my [blog](http://bulimov.ru) sources. Using [Pelican](http://getpelican.com).

# setting everything up

1. Install python3
2. Install pelican and markdown from pip `pip3 install pelican markdown`
3. Clone pelican-plugins and pelican themes repos
    ```shell
mkdir -p ~/github && \
git clone --recursive https://github.com/getpelican/pelican-plugins ~/github/pelican-plugins && \
git clone --recursive https://github.com/getpelican/pelican-themes ~/github/pelican-themes
    ```
4. Link pelican-bootstrap3 theme `pelican-themes -s ~/github/pelican-themes/pelican-bootstrap3`
5. Ensure that you have ~/github/pelican-plugins in $PYTHONPATH
