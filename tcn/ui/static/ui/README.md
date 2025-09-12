# UI Styles

Basic commands to get started.

First `cd` into dir:

```console
cd tcn/ui/static/ui
```

To generate the styles:

```console
npm install
cd tcn/ui/static/ui
npx @tailwindcss/cli -i ../static/ui/css/app.css -o ../static/ui/css/styles.css --cwd ../../templates -m -w
```

To format the templates:

```console
npx prettier -w ../../templates
```
