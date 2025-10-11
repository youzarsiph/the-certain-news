# UI Styles

Basic commands to get started.

First `cd` into dir:

```console
cd tcn/ui/static/tcn
```

To generate the styles:

```console
npm install
cd tcn/ui/static/tcn
npx @tailwindcss/cli -i ../static/tcn/css/app.css -o ../static/tcn/css/styles.css --cwd ../../templates -m -w
```

To format the templates:

```console
npx prettier -w ../../templates
```
