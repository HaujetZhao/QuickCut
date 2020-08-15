## Translation Help

### Before Translate

Each class of the QuickCut is a part of translation. Check out whick part is under translation in issue page. If you decide to translate some parts, please first open an issue to notify every that this part is under work, so that others won't repeat the wheels. 

### How to Translate

Different language translation have the same process, so I'll just take translating to English as example.

First make sure you have `pyside2` installed by executing `pip install pyside2`

![image-20200731135839898](assets/image-20200731135839898.png)

If you are on Windows, run `create_ts.bat`, it will read the config from `project.pro`, and then generate a `en.ts` file, which can be opened by `Linguist` .

After installing `PySide2`, the `Linguist` is also installed, you just run `linguist` in command line, it will launch. 

Use `Linguist` to open `en.ts`, and then translate the items: 

![image-20200731135944600](assets/image-20200731135944600.png) 

After translating each item, don't forget to click the `√` to tell `Linguist` that this item translation is complete, and most importantly, add it to the dictionary `en.qph` by pressing `Ctrl + T` . 

The next time `QuickCut` commits, you may need to run `create_ts.bat` again, the `en.ts` will be updated, but the translation inside of it will also be deleted. 

You can use the dictionary `en.qph` (which you have added translated items to it) to quickly fill blanks by using `Linguist`'s batch translation: 

![image-20200731140036406](assets/image-20200731140036406.png)

After that, use `Linguist` to generated a `en.qm` which is the final language file can be load by `QuickCut.py`

When your translation is finished, you can pull a request to the [QuickCut](https://github.com/HaujetZhao/QuickCut). Or send an email to 1292756898@qq.com 