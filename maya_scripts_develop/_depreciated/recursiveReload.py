'''
Created on 2012-02-25
 
@author: Mat
'''
 
import sys
import inspect
 
from distutils import sysconfig
from types import ModuleType
 
_processedModules = set()
_importedModules = set()
_remappingData = list()
 
class ImportRemapData(object):
 
    def __init__(
        self,
        destModuleName,
        destAttrName,
        sourceModuleName,
        sourceAttrName,
        attrType
        ):
 
        self._destModuleName = destModuleName
        self._destAttrName = destAttrName
        self._sourceModuleName = sourceModuleName
        self._sourceAttrName = sourceAttrName
        self._attrType = attrType
 
    def remap(self):
        '''
        This gets the new modules and assigns the new attr value to the
        attr name in the new destination module.
        '''
 
        #get the newly reloaded source module and then the new attr value
        sourceModule = sys.modules[self._sourceModuleName]
 
        #we need to get the new attr value as well
        newAttrVal = None
        #if the new attr val is a module, we need to get the module from sys
        if self._attrType == ModuleType:
            newAttrVal = sys.modules[self._sourceAttrName]
        #otherwise, just get it from the new source module
        else:
            newAttrVal = getattr(sourceModule, self._sourceAttrName)
 
        #get the newly reloaded destination module and set the new attr value
        destModule = sys.modules[self._destModuleName]
        setattr(destModule, self._destAttrName, newAttrVal)
 
def recursiveReload(module, debug=False):
 
    #get all of the data necessary for full reload of the module
    _getModuleData(module)
 
    #reload all of the collected modules
    for importedModule in _importedModules:
        if debug:
            print 'Reloading module: %s' % importedModule
        reload(importedModule)
 
    #now that the modules are all reloaded, re-map the extra data
    for remapData in _remappingData:
        remapData.remap()
 
    #clear our variables for future use
    _processedModules.clear()
    _importedModules.clear()
    del _remappingData[:]
 
    return True
 
def _getModuleData(module):
    '''
    Inspects the module and all of its sub-modules to get all imported modules
    and data required for us to re-map variables properly.
    '''
 
    #add this module to the list of processed modules so we do not try to
    #process it again and risk getting into an infinite loop
    _processedModules.add(module)
 
    #get all attr names from the module
    attrNames = dir(module)
 
    detectedModules = set()
    for attrName in attrNames:
 
        #get attr value and try to get the module where the value originated from
        attrVal = getattr(module, attrName)
        attrModule = inspect.getmodule(attrVal)
 
        #if we didn't get a module returned, we are dealing with a builtin, or
        #we are dealing with this module skip to the next loop iteration.
        #We need to do two checks for builtin modules, if it is in the builtin
        #module names and if it does not have a __file__ attr.
        if not attrModule \
        or attrModule.__name__ in sys.builtin_module_names \
        or not hasattr(attrModule, '__file__') \
        or attrModule == sys.modules[__name__]:
            continue
 
        #we also do not want to reload if the module comes from the standard lib
        #to check for this, we need to get the module's path and check that it
        #is in the lib folder, but not in the site packages folder
        moduleFilepath = attrModule.__file__.lower()
        pyStdLib = sysconfig.get_python_lib(standard_lib=True).lower()
        pySitePkg = sysconfig.get_python_lib().lower()
 
        if moduleFilepath.startswith(pyStdLib) \
        and not moduleFilepath.startswith(pySitePkg):
            continue
 
        #add the module to the list of modules that have been imported
        detectedModules.add(attrModule)
 
        #if the attr value does not have a name attr, skip to the next iteration
        if not hasattr(attrVal, '__name__'):
            continue
 
        #if the module where the attr value came from is different from the
        #current module, collect data we need to remap things
        origName = attrVal.__name__
        if attrModule != module:
            #print module.__name__, attrName, attrModule.__name__, origName
            remapData = ImportRemapData(
                module.__name__,
                attrName,
                attrModule.__name__,
                origName,
                type(attrVal)
                )
            _remappingData.append(remapData)
 
    #add the detected modules to the imported modules set
    _importedModules.update(detectedModules)
 
    #cycle through the modules we detected, which have not already been processed
    #and process them as well
    for detectedModule in detectedModules:
 
        if detectedModule in _processedModules:
            continue
 
        _getModuleData(detectedModule)
 
    return True