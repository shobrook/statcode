# httphelp

`httphelp` is like `man` but for HTTP status codes and headers. Most web developers spend considerable time looking at response codes (usually errors) and then Googling what they mean. But with `httphelp`, you can simply run `$ httphelp [status_code]` and get a quick explanation of your HTTP response without leaving the terminal. Also, for add value, you can check the meaning of any header you might find in your request or response.

![demo](assets/demo.gif)

## Installation

`httphelp` works on MacOS, Linux, and Windows, with compiled binaries available for [every release](https://github.com/Malex/statcode/releases). You can also install it with pip:

`$ pip install httphelp`

Requires Python 3.0 or higher.

## Contributing

This is based on (or, rather, forked from) a small project (statcode, something @shobrook put together on a plane ride), but I intend to turn this into a go-to manual for everything related to HTTP. For example, it should so be possible to get a link for the specific RFC relative to a given header or status code. If you'd like to be a part of that, feel free to make a contribution – just fork the repo, make your changes and then submit a pull request. If you do contribute, just fork and send a pull request, I'll try to answer to it fast.

If you've discovered a bug or have a feature request, create an [issue](https://github.com/Malex/statcode/issues/new) and I'll take care of it!
