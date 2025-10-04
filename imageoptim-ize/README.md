# ImageOptim-ize

This workflow is designed to streamline the process of optimizing images directly from the Finder. It works in MacOS only, because [Alfred](https://www.alfredapp.com/) works in MacOS only.

By selecting one or more images and triggering the workflow with a designated hotkey (default is ctrl+shft+cmd+I), users can automatically process their selected images using [ImageOptim](https://imageoptim.com/mac) .

The workflow begins by sending a notification to inform the user that image optimization is in progress. It then iterates over each selected image file, invoking ImageOptim to remove unnecessary metadata and reduce file size efficiently.

Once the optimization process is complete, a final notification is displayed, confirming the successful optimization of the images.

All you need is the .alfredworkflow file to install and use—I just included the zsh script so it could be edited and version-controlled externally before being dropped back in to Alfred. The script in this directory is exactly what's in the workflow.

[ziad@feralcreative.dev](mailto:ziad@feralcreative.dev)
