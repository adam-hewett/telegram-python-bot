var fs = require("fs");
var resolve = require("path").resolve;
var join = require("path").join;
var cp = require("child_process");
var os = require("os");

var lib = resolve(__dirname, ".");

var checkPackageJSON = function (mod) {
    var modPath = join(lib, mod, "nodejs");

    if (!fs.existsSync(join(modPath, "package.json"))) return;

    var npmCMD = os.platform().startsWith("win") ? "npm.cmd" : "npm";

    cp.spawn(npmCMD, ["i"], { env: process.env, cwd: modPath, stdio: "inherit" });
};

var checkRequirementsTXT = function (mod) {
    var modPath = join(lib, mod, "python");

    if (!fs.existsSync(join(modPath, "requirements.txt"))) return;

    var pip3CMD = os.platform().startsWith("win") ? "pip3" : "pip3";

    cp.spawn(pip3CMD, ["install", "-r", "requirements.txt", "-t", "pip_modules"], {
        env: process.env,
        cwd: modPath,
        stdio: "inherit",
    });
};

fs.readdirSync(lib).forEach(function (mod) {
    checkPackageJSON(mod);

    checkRequirementsTXT(mod);
});
