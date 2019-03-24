/**
 * A simple plugin that implements DALME specific functionality for Diva.js. Plugins
 * should register themselves as a class in the global Diva namespace, e.g., global.Diva.MetadataPlugin.
 * Plugins are then included as *uninstantiated* references within a plugin configuration. To enable them, simply include
 * plugins: [Diva.MetadataPlugin] when creating a Diva instance.
 * When the viewer is instantiated it will also instantiate the plugin, which
 * will then configure itself.
 *
 * Plugin constructors should take one argument, which is an instance of a ViewerCore object.
 *
 *
 * Plugins should implement the following interface:
 *
 * {boolean} isPageTool - Added to the class prototype. Whether the plugin icon should be included for each page as a page tool
 * {string} pluginName - Added to the class prototype. Defines the name for the plugin.
 *
 * @method createIcon - A div representing the icon. This *should* be implemented using SVG.
 * @method handleClick - The click handler for the icon.
 *
 * Toolbar plugins must have a toolbarIcon and toolbarSide attribute, with toolbarSide being either 'left' or 'right'
 **/

export default class DalmePlugin
{
    constructor (core)
    {
        this.core = core;

    }
}

DalmePlugin.prototype.pluginName = "DALME";
DalmePlugin.prototype.isPageTool = false;
/* Make this plugin available in the global context
 * as part of the 'Diva' namespace.*/
(function (global)
{
    global.Diva.DalmePlugin = DalmePlugin;
})(window);
