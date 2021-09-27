var fs = require("fs");
var resolve = require("path").resolve;
var join = require("path").join;
var cp = require("child_process");
var os = require("os");

var lib = resolve(__dirname, ".");

var updatePackageJSON = function (mod) {
    var modPath = join(lib, mod, "nodejs");

    if (!fs.existsSync(join(modPath, "package.json"))) return;

    var ncuCMD = os.platform().startsWith("win") ? "ncu" : "ncu";
    var npmCMD = os.platform().startsWith("win") ? "npm.cmd" : "npm";
    var rmCMD = os.platform().startsWith("win") ? "del" : "rm";

    var childNCU = cp.spawn(ncuCMD, ["-u"], { env: process.env, cwd: modPath, stdio: "inherit" });
    childNCU.on("exit", function () {
        var childRM = cp.spawn(rmCMD, ["package-lock.json"], { env: process.env, cwd: modPath, stdio: "inherit" });

        childRM.on("exit", function () {
            cp.spawn(npmCMD, ["i"], { env: process.env, cwd: modPath, stdio: "inherit" });
        });
    });
};

var updateRequirementsTXT = function (mod) {
    var modPath = join(lib, mod, "python");

    if (!fs.existsSync(join(modPath, "requirements.txt"))) return;

    var pip3Cmd = os.platform().startsWith("win") ? "pip3" : "pip3";

    cp.spawn(pip3Cmd, ["install", "-r", "requirements.txt", "-t", "pip_modules", "--upgrade"], {
        env: process.env,
        cwd: modPath,
        stdio: "inherit",
    });
};

fs.readdirSync(lib).forEach(function (mod) {
    updatePackageJSON(mod);

    updateRequirementsTXT(mod);
});
