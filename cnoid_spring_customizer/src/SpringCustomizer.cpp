#include <stdlib.h>

#include <cmath>
#include <cstring>
#include <fstream>
#include <boost/function.hpp>
#include <boost/bind.hpp>
#include <yaml-cpp/yaml.h>

#include <cnoid/BodyCustomizerInterface>
#include <iostream>

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif /* Windows */

//cnoid::Matrix3 trans(const cnoid::Matrix3& M) { return M.transpose(); }
//double dot(const cnoid::Vector3& a, const cnoid::Vector3& b) { return a.dot(b); }
//typedef cnoid::Matrix3 Matrix33;

using namespace std;
using namespace boost;
using namespace cnoid;

static BodyInterface* bodyInterface = 0;

static BodyCustomizerInterface bodyCustomizerInterface;

struct JointValSet
{
    double* valuePtr;
    double* velocityPtr;
    double* torqueForcePtr;
    // JointInfo
    std::string name;
    double K;
    double D;
    double upper_limit;
    double lower_limit;
};

struct SpringCustomizer
{
    BodyHandle bodyHandle;

    std::vector<JointValSet > jointValSets;
};


static const char** getTargetModelNames()
{
    char *rname = getenv("SPRING_CUSTOMIZER_ROBOT");
    if (rname != NULL) {
        std::cerr << "SPRING_CUSTOMIZER_ROBOT =" << rname << std::endl;
    }
    static const char* names[] = {
        rname,
        0 };

    return names;
}

static BodyCustomizerHandle create(BodyHandle bodyHandle, const char* modelName)
{
    SpringCustomizer* customizer = 0;

    std::cerr << "create SpringCustomizer : " << std::string(modelName) << std::endl;
    customizer = new SpringCustomizer;
    customizer->jointValSets.resize(0);
    customizer->bodyHandle = bodyHandle;

    char* config_file_path = getenv("SPRING_CUSTOMIZER_CONF_FILE");
    if (config_file_path) {
        ifstream ifs(config_file_path);
        if (ifs.is_open()) {
            JointValSet vs;
            std::cerr << "[SpringCustomizer] Config file is: " << config_file_path << std::endl;
            YAML::Node param = YAML::LoadFile(config_file_path);
            try {
                if (!param.IsMap()) {
                    std::cerr << "[SpringCustomizer] file does not contain a map" << std::endl;
                    return static_cast<BodyCustomizerHandle>(customizer);
                }
                YAML::Node sp_lst = param["springs"];// list
                if (!sp_lst.IsSequence()) {
                    std::cerr << "[SpringCustomizer] springs is not a sequence" << std::endl;
                    return static_cast<BodyCustomizerHandle>(customizer);
                }
                for(int i = 0; i < sp_lst.size(); i++) {
                    const YAML::Node &sp = sp_lst[i];

                    vs.name = sp["joint_name"].as<std::string>();
                    vs.K = sp["K"].as<double>();
                    vs.D = sp["D"].as<double>();
                    vs.upper_limit = sp["upper_limit"].as<double>();
                    vs.lower_limit = sp["lower_limit"].as<double>();

                    int index = bodyInterface->getLinkIndexFromName(bodyHandle, vs.name.c_str());
                    if (index < 0) {
                        std::cerr << "[SpringCustomizer] failed to find joint: " << vs.name << std::endl;
                        continue;
                    }
                    vs.valuePtr = bodyInterface->getJointValuePtr(bodyHandle, index);
                    vs.velocityPtr = bodyInterface->getJointVelocityPtr(bodyHandle, index);
                    vs.torqueForcePtr = bodyInterface->getJointForcePtr(bodyHandle, index);
                    std::cerr << "[SpringCustomizer] add joint_name: " << vs.name << std::endl;
                    std::cerr << "[SpringCustomizer]     K: " << vs.K << std::endl;
                    std::cerr << "[SpringCustomizer]     D: " << vs.D << std::endl;
                    std::cerr << "[SpringCustomizer]     upper_limit: " << vs.upper_limit << std::endl;
                    std::cerr << "[SpringCustomizer]     lower_limit: " << vs.lower_limit << std::endl;
                    customizer->jointValSets.push_back(vs);
                }
            } catch (YAML::Exception &e) {
                std::cerr << "[SpringCustomizer] yaml read error: " << e.what() << std::endl;
            }
        } else {
            std::cerr << "[SpringCustomizer] " << config_file_path << " is not found" << std::endl;
        }
    }

    return static_cast<BodyCustomizerHandle>(customizer);
}


static void destroy(BodyCustomizerHandle customizerHandle)
{
    SpringCustomizer* customizer = static_cast<SpringCustomizer*>(customizerHandle);
    if(customizer){
        delete customizer;
    }
}

static void setVirtualJointForces(BodyCustomizerHandle customizerHandle)
{
    SpringCustomizer* customizer = static_cast<SpringCustomizer*>(customizerHandle);
    for(int i=0; i < customizer->jointValSets.size(); ++i) {
        JointValSet& trans = customizer->jointValSets[i];
        *(trans.torqueForcePtr) = - trans.K * (*trans.valuePtr) - trans.D * (*trans.velocityPtr);
    }
}

extern "C" DLL_EXPORT
cnoid::BodyCustomizerInterface* getHrpBodyCustomizerInterface(cnoid::BodyInterface* bodyInterface_)
{
    bodyInterface = bodyInterface_;

    bodyCustomizerInterface.version = cnoid::BODY_CUSTOMIZER_INTERFACE_VERSION;
    bodyCustomizerInterface.getTargetModelNames = getTargetModelNames;
    bodyCustomizerInterface.create = create;
    bodyCustomizerInterface.destroy = destroy;
    bodyCustomizerInterface.initializeAnalyticIk = NULL;
    bodyCustomizerInterface.calcAnalyticIk = NULL;
    bodyCustomizerInterface.setVirtualJointForces = setVirtualJointForces;

    return &bodyCustomizerInterface;
}
