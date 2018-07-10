# statcode

`statcode` pages are like `man` pages but for HTTP status codes. Most web developers spend considerable time looking at response codes (usually errors) and then Googling what they mean. But with `statcode`, you can simply run `$ statcode [status_code]` and get a quick explanation of your HTTP response – without leaving the terminal.

![demo](assets/demo.gif)

## Installation

`statcode` works on MacOS, Linux, and Windows (if you use Cygwin), with compiled binaries available for [every release](https://github.com/shobrook/statcode/releases). You can also install it with pip:

`$ pip install statcode`

Requires Python 3.0 or higher.

## Contributing

This was something I put together on a plane ride, but I intent to turn this project into a go-to manual for everything related to HTTP. For example, it should soon be possible to look up different [request headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers), i.e. running `$ statcode cache-control` and getting "Specifies directives for caching mechanisms in both requests and responses." If you'd like to be a part of that, feel free to make a contribution – just fork the repo, make your changes and then submit a pull request. If you do contribute, please try to adhere to the existing style.

If you've discovered a bug or have a feature request, create an [issue](https://github.com/shobrook/statcode/issues/new) and I'll take care of it!
