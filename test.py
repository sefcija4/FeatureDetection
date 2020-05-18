#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import app

test_path = 'test'


def main():

    app.main(os.path.join(test_path, 'config1.json'))
    # app.main('config2.json')
    # app.main('config3.json')
    app.main(os.path.join(test_path, 'config4.json'))
    app.main(os.path.join(test_path, 'config5.json'))
    # app.main(os.path.join(test_path, 'config6.json'))
    app.main(os.path.join(test_path, 'config7.json'))
    app.main(os.path.join(test_path, 'config8.json'))
    app.main(os.path.join(test_path, 'config9.json'))
    app.main(os.path.join(test_path, 'config10.json'))
    app.main(os.path.join(test_path, 'config11.json'))
    app.main(os.path.join(test_path, 'config12.json'))
    # app.main('config11.json')


if __name__ == "__main__":
    main()
