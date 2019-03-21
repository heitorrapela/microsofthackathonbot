// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

const _ = require('lodash');
const mkdirp = require('mkdirp');
const path = require('path');

const { commonFilesWriter } = require('./commonFilesWriter');
const { BOT_TEMPLATE_NAME_SIMPLE,  BOT_TEMPLATE_NOPROMPT_SIMPLE } = require('./constants');

// generators/app/templates folder name
const GENERATOR_TEMPLATE_NAME = 'echo';

const LANG_TS = 'typescript';

/**
 * Write the files that are specific to the echo bot template
 *
 * @param {Generator} gen Yeoman's generator object
 * @param {String} templatePath file path to write the generated code
 */
const writeEchoTemplateFiles = (gen, templatePath) => {
  const DEPLOYMENT_SCRIPTS = 0;
  const DEPLOYMENT_MSBOT = 1;
  const TS_SRC_FOLDER = 'src'
  const folders = [
    'deploymentScripts',
    path.join('deploymentScripts', 'msbotClone')
  ];
  const extension = _.toLower(gen.props.language) === 'javascript' ? 'js' : 'ts';
  const srcFolder = _.toLower(gen.props.language) === 'javascript' ? '' : TS_SRC_FOLDER;

  // create the echo bot folder structure common to both languages
  for (let cnt = 0; cnt < folders.length; ++cnt) {
    mkdirp.sync(folders[cnt]);
  }
  // create a src directory if we are generating TypeScript
  if (_.toLower(gen.props.language) === LANG_TS) {
    mkdirp.sync(TS_SRC_FOLDER);
  }

  let sourcePath = path.join(templatePath, folders[DEPLOYMENT_SCRIPTS]);
  let destinationPath = path.join(gen.destinationPath(), folders[DEPLOYMENT_SCRIPTS]);

   // if we're writing out TypeScript, then we need to add a webConfigPrep.js
   if(_.toLower(gen.props.language) === LANG_TS) {
     gen.fs.copy(
       path.join(sourcePath, 'webConfigPrep.js'),
       path.join(destinationPath, 'webConfigPrep.js')
     );
   }

  // write out deployment resources
  sourcePath = path.join(templatePath, folders[DEPLOYMENT_MSBOT]);
  destinationPath = path.join(gen.destinationPath(), folders[DEPLOYMENT_MSBOT]);
  gen.fs.copyTpl(
    path.join(sourcePath, 'bot.recipe'),
    path.join(destinationPath, 'bot.recipe'),
    {
      botname: gen.props.botname
    }
  );

  // write out the index.js and bot.js
  destinationPath = path.join(gen.destinationPath(), srcFolder);

  // gen the main index file
  gen.fs.copyTpl(
    gen.templatePath(path.join(templatePath, `index.${extension}`)),
    path.join(destinationPath, `index.${extension}`),
    {
      botname: gen.props.botname
    }
  );

  // gen the main bot activity router
  gen.fs.copy(
    gen.templatePath(path.join(templatePath, `bot.${extension}`)),
    path.join(destinationPath, `bot.${extension}`)
  );

  // write out PREREQUISITES.md
  gen.fs.copyTpl(
    gen.templatePath(path.join(templatePath, 'PREREQUISITES.md')),
    gen.destinationPath('PREREQUISITES.md'),
    {
      botname: gen.props.botname
    }
  );
}

/**
 * Write project files for Echo template
 *
 * @param {Generator} gen Yeoman's generator object
 */
module.exports.echoTemplateWriter = gen => {
  // do some simple sanity checking to ensure we're being
  // called correctly
  const template = _.toLower(gen.props.template)
  if (template !== _.toLower(BOT_TEMPLATE_NAME_SIMPLE) && template !== _.toLower(BOT_TEMPLATE_NOPROMPT_SIMPLE)) {
    throw new Error(`writeEchoProjectFiles called for wrong template: ${ gen.props.template }`);
  }

  // build the path to the echo template source folder
  const templatePath = path.join(gen.templatePath(), GENERATOR_TEMPLATE_NAME);

  // write files common to all our template options
  commonFilesWriter(gen, templatePath);

  // write files specific to the echo bot template
  writeEchoTemplateFiles(gen, templatePath);
}

