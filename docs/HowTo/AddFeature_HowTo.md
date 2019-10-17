# How To Add a Feature
## Add feature to Extractor class in Extractor.py
1. Add the feature method to the Extractor class in Extractor.py.
2. Add the feature to the featureSwitcher dictionary in the __init__.py file in the FeatureExtraction package.
    -   The dictionary entry consists of two parts:
        1. The feature name
        2. The method and parameters

## Add new Extractor class that extends default Extractor class
1. Create new feature extractor class.
2. Add an import statement into __init__.py to import extractor class.
3. Add class name to the dictionary in the extractorSwitcher function.
4. Add the new feature(s) to the featureSwitcher dictionary in the __init__.py file.
    -   The dictionary entry consists of two parts:
        1. The feature name
        2. The method and parameters