# teen

`teen` pages are like `man` pages but for HTTP status codes. Most web developers spend considerable time looking at response codes (usually errors) and then Googling what they mean. But with `teen`, you can simply run `$ teen [status_code]` and get a quick explanation of your HTTP response – without leaving the terminal.

![demo](assets/demo.gif)

## Installation

Teen works on MacOS, Linux, and Windows (if you use Cygwin), with compiled binaries available for [every release](https://github.com/shobrook/teen/releases). You can also install it with pip:

`$ pip install teen`

Requires Python 3.0 or higher.

## Contributing

This was just something I put together in a day, but eventually I'd like to turn this project into the go-to manual for everything related to HTTP, such as extending support to things like [request headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers). If you'd like to be a part of that, feel free to make a contribution. Just fork the repo, make your changes and then submit a pull request. If you do contribute, please try to adhere to the existing style.

If you've discovered a bug or have a feature request, create an [issue](https://github.com/shobrook/teen/issues/new) and I'll take care of it!
