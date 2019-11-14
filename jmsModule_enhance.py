from java.io import FileInputStream


def createJMSModule(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,serverTarget) = items
    
    # Check if JMS Module already exist
    redirect('/dev/null','false')
    exist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName in exist:
      print('!!! JMS Modules ' + moduleName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Create new JMS Module
    cmo.createJMSSystemResource(moduleName)
    
    # Set Up Target server/cluster
    cd('/JMSSystemResources/' + moduleName)
    targetsForDeployment = []
    targets = serverTarget.split('|')
    for target in targets: 
      if(target == '') :
        break;
      index=target.find(':')
      serverName=target[0:index]
      type=target[index+1:]
      nextName =str('com.bea:Name='+serverName+',Type='+type)
      targetsForDeployment.append(ObjectName(nextName))
    set('Targets',jarray.array(targetsForDeployment, ObjectName))

    # Print output
    print('# JMS Module: ' + moduleName)

    save()
    activate()
	
  except Exception, e:
    print e


def createSubdeploy(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,subdepName,serverTarget) = items
	
    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Subdeployment already exist
    cd('/JMSSystemResources/' + moduleName  )
    redirect('/dev/null','false')
    exist = ls('SubDeployments',returnMap='true')
    if subdepName in exist:
      print('!!! Subdeployment ' + subdepName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Foreign Name
    cmo.createSubDeployment(subdepName)

    # Set Up Target server/cluster
    if serverTarget != '':
      cd('/JMSSystemResources/' + moduleName + '/SubDeployments/' + subdepName )
      targetsForDeployment = []
      targets = serverTarget.split('|')
      for target in targets: 
        if(target == '') :
          break;
        index=target.find(':')
        serverName=target[0:index]
        type=target[index+1:]
        nextName =str('com.bea:Name='+serverName+',Type='+type)
        targetsForDeployment.append(ObjectName(nextName))
      set('Targets',jarray.array(targetsForDeployment, ObjectName))
    else:
      print('Not Target Subdeployment: ' + sebdepName)	

    # Print output
    print('# Module: ' + moduleName )
    print('# Subdeployment: ' + subdepName )

    save()
    activate()
	
  except Exception, e:
    print e


def createForeignServer(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,foreignName,jndiInitConnFac,jndiConUrl) = items
	
    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Foreign Server already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('ForeignServers',returnMap='true')
    if foreignName in exist:
      print('!!! Foreign Server ' + foreignName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Foreign Name
    cmo.createForeignServer(foreignName)
	
    # Set Initial Context Factory and Connection URL
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/' + foreignName)
	
    cmo.setInitialContextFactory(jndiInitConnFac)
    cmo.setConnectionURL(jndiConUrl)
	
    print('# Module: ' + moduleName)
    print('# Foreign Server: ' + foreignName)
    print('# Foreign JNDI Initial Context Factory: ' + jndiInitConnFac)
    print('# Foreign JNDI Connection URL: ' + jndiConUrl)

    save()
    activate()

  except Exception, e:
    print e



def createQueues(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,queueName,jndiQueue,subdepName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Queue Server already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('Queues',returnMap='true')
    if queueName in exist:
      print('!!! Queue: ' + queueName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Queue
    cmo.createQueue(queueName)
    
    # Set JNDI Name Queue
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/Queues/' + queueName )
    cmo.setJNDIName(jndiQueue)
	
    # Set Subdeployment if exist in csv
    if subdepName != '' and subdepName != 'default':	
      print('# Subdeployment Queue: ' + subdepName)
      cmo.setSubDeploymentName(subdepName)	  
    else:
      print('!!! Subdeployment Queue Not Set')
	
    # Print output
    print('# Module: ' + moduleName )
    print('# Queue: ' + queueName )
    print('# JNDI Name Queue: ' + jndiQueue)
	
    save()
    activate()
	
  except Exception, e:
    print e


def createDistQueueUniform(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,distQueueName,jndiDistQueue,subdepName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Distributed Queue already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('DistributedQueues',returnMap='true')
    if distQueueName in exist:
      print('!!! Distributed Queue ' + distQueueName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Distributed Queue
    cmo.createUniformDistributedQueue(distQueueName)
	
    # Set JNDI Distributed Queue
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/UniformDistributedQueues/' + distQueueName)
    cmo.setJNDIName(jndiDistQueue)
    
    # Set Subdeployment if exist in csv
    if subdepName != '' and subdepName != 'default':
      print('# Set Subdeployment Queue: ' + subdepName)
      cmo.setSubDeploymentName(subdepName)
    elif subdepName == 'default':
      cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/UniformDistributedQueues/' + distQueueName)
      print('# Set Subdeployment to default')
      cmo.setDefaultTargetingEnabled(true)
    else:
      print('# Subdeployment Topic Not Set')

    # Print output
    print('# Mudule Name: ' + moduleName )
    print('# Uniform Distributed Queue: ' + distQueueName )
    print('# JNDI Distributed Queue: ' + jndiDistQueue )

    save()
    activate()
	
  except Exception, e:
    print e



def createDistQueueWeighted(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,distQueueName,jndiDistQueue,queueName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!\n')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Distributed Queue already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('DistributedQueues',returnMap='true')
    if distQueueName in exist:
      print('!!! Distributed Queue ' + distQueueName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Distributed Queue
    cmo.createDistributedQueue(distQueueName)
	
    # Set JNDI Distributed Queue
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/DistributedQueues/' + distQueueName)
    cmo.setJNDIName(jndiDistQueue)

    targets = queueName.split('|')
    for target in targets: 
      if(target == '') :
        break;
      print('# Add Weighted Distributed Member Queue: ' + target )
      cmo.createDistributedQueueMember(target)
    
    # Print output
    print('# Module Name: ' + moduleName )
    print('# Weighted Distributed Queue: ' + distQueueName )
    print('# Weighted Distributed Queue JNDI: ' + jndiDistQueue )
	
    save()
    activate()
	
  except Exception, e:
    print e
	

def createTopic(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,topicName,jndiTopic,subdepName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')	
	
    # Check if Topic Server already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('Topics',returnMap='true')
    if topicName in exist:
      print('!!! Queue: ' + topicName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Topic
    cmo.createTopic(topicName)
    
    # Set JNDI Name Topic
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/Topics/' + topicName )
    cmo.setJNDIName(jndiTopic)

    # Set Subdeployment if exist in csv
    if subdepName != '':
      cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/Topics/' + topicName )
      print('# Set Subdeployment Topic: ' + subdepName)
      cmo.setSubDeploymentName(subdepName)
    else:
      print('# Subdeployment Topic Not Set')
	
    # Print output
    print('# Module Name: ' + moduleName )	
    print('# Topic Name: ' + topicName )	
    print('# JNDI Name Topic: ' + jndiTopic)
	
    save()
    activate()
	
  except Exception, e:
    print e


def createDistTopicUniform(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,distTopicName,jndiDistTopic,subdepName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Distributed Topic already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('DistributedTopics',returnMap='true')
    if distTopicName in exist:
      print('!!! Distributed Topic ' + distTopicName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Distributed Topic
    cmo.createUniformDistributedTopic(distTopicName)
	
    # Set JNDI Distributed Topic
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/UniformDistributedTopics/' + distTopicName)
    cmo.setJNDIName(jndiDistTopic)
    
    # Set Subdeployment if exist in csv
    if subdepName != '' and subdepName != 'default':
      print('# Set Subdeployment Topic: ' + subdepName)
      cmo.setSubDeploymentName(subdepName)
    elif subdepName == 'default':
      cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/UniformDistributedTopics/' + distTopicName)
      print('# Set Targetting to default')
      cmo.setDefaultTargetingEnabled(true)
    else:
      print('!!! Subdeployment Distributed Topic Uniform Not Set')

    # Print output
    print('# Module Name: ' + moduleName )
    print('# Uniform Distributed Topic: ' + distTopicName )
    print('# JNDI Uniform Distributed Topic: ' + jndiDistTopic)

    save()
    activate()
	
  except Exception, e:
    print e



def createDistTopicWeighted(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,distTopicName,jndiDistTopic,queueName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Distributed Topic already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('DistributedTopics',returnMap='true')
    if distTopicName in exist:
      print('!!! Distributed Topic ' + distTopicName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Distributed Topic
    cmo.createDistributedTopic(distTopicName)
	
    # Set JNDI Distributed Topic
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/DistributedTopics/' + distTopicName)
    cmo.setJNDIName(jndiDistTopic)

    targets = queueName.split('|')
    for target in targets: 
      if(target == '') :
        break;
      print('# Add Weighted Distributed Member Topic: ' + target )
      cmo.createDistributedTopicMember(target)
    
    # Print output
    print('# Module Name: ' + moduleName )
    print('# Weighted Distributed Topic: ' + distTopicName )
    print('# Weighted Distributed Topic JNDI: ' + jndiDistTopic )
	
    save()
    activate()
	
  except Exception, e:
    print e


def createConnFactory(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,connFactoryName,jndiconnFactory,attachJMSXUserId,clientIdPolicy,subscriptionSharingPolicy,messagesMaximum,XAConnectionFactoryEnabled,subdepName) = items

    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!\n')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Connection Factory already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('ConnectionFactories',returnMap='true')
    if connFactoryName in exist:
      print('!!! Connection Factory ' + connFactoryName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Connection Factory
    cmo.createConnectionFactory(connFactoryName)
	
    # Set JNDI Connection Factory
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ConnectionFactories/' + connFactoryName)
    cmo.setJNDIName(jndiconnFactory)

    # Set Subdeployment if exist in csv
    if subdepName != '':
      cmo.setSubDeploymentName(subdepName)
    elif subdepName == 'default':
      cmo.setDefaultTargetingEnabled(true)
    else:
      print('\nSubdeployment Topic Not Set')
	
    # Set Attach JMSX User ID
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ConnectionFactories/' + connFactoryName + '/SecurityParams/' + connFactoryName)
    cmo.setAttachJMSXUserId(int(attachJMSXUserId))

    
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ConnectionFactories/' + connFactoryName + '/ClientParams/' + connFactoryName)
    cmo.setClientIdPolicy(clientIdPolicy)
    cmo.setSubscriptionSharingPolicy(subscriptionSharingPolicy)
    cmo.setMessagesMaximum(int(messagesMaximum))
	
    
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ConnectionFactories/' + connFactoryName + '/TransactionParams/' + connFactoryName)
    cmo.setXAConnectionFactoryEnabled(int(XAConnectionFactoryEnabled))

    # Print output
    print('# Module Name: ' + moduleName )
    print('# Connection Factory: ' + connFactoryName )
    print('# JNDI Connection Factory: ' + jndiconnFactory )
    print('# Attach JMSX User ID: ' + ['false','true'][attachJMSXUserId == '1'] )
    print('# Client ID Policy: ' + clientIdPolicy )
    print('# Subscription Sharing Policy: ' + str(subscriptionSharingPolicy) )
    print('# Mesages Maximum: ' + str(messagesMaximum) )
    print('# XA Connection Factory Enabled: ' + ['false','true'][XAConnectionFactoryEnabled == '1'] )

    save()
    activate()
	
  except Exception, e:
    print e
	
	

def createForeignDest(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,foreignName,foreignDestName,localJNDIName,remoteJNDIName) = items
	
    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + '  !!!')
      exit(exitcode=1,defaultAnswer='y')
    
    # Check if Foreign name correct
    redirect('/dev/null','false')
    forExist = ls('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/',returnMap='true')
    if foreignName not in forExist:
      print('!!! Wrong Foreign Name :' + foreignName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')	  

    # Check if foreign Destination name already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/' + foreignName)
    redirect('/dev/null','false')
    exist = ls('ForeignDestinations',returnMap='true')
    if foreignDestName in exist:
      print('!!! Foreign Destination ' + foreignDestName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Foreign Destination 
    cmo.createForeignDestination(foreignDestName)
	
    # Set Local and Remote JNDI for Foreign Destination Name
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/' + foreignName + '/ForeignDestinations/' + foreignDestName)
    cmo.setLocalJNDIName(localJNDIName)
    cmo.setRemoteJNDIName(remoteJNDIName)
	
    # Print output
    print('# Module Name: ' + moduleName )
    print('# Foreign Destination: ' + foreignDestName)
    print('# Local JNDI Name: ' + localJNDIName)
    print('# Remote JNDI Name: ' + remoteJNDIName)

    save()
    activate()

  except Exception, e:
    print e



def createforeignConnFactName(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,foreignName,foreignConnFactName,localJNDIName,remoteJNDIName) = items
	
    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
    
    # Check if Foreign name correct
    redirect('/dev/null','false')
    forExist = ls('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/',returnMap='true')
    if foreignName not in forExist:
      print('!!! Wrong Foreign Name :' + foreignName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
	
    # Check if Foreign Name already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/' + foreignName)
    redirect('/dev/null','false')
    exist = ls('ForeignConnectionFactories',returnMap='true')
    if foreignConnFactName in exist:
      print('!!! Foreign Connection Factory ' + foreignConnFactName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Foreign Destination 
    cmo.createForeignConnectionFactory(foreignConnFactName)
	
    # Set Local and Remote JNDI Name
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/ForeignServers/' + foreignName + '/ForeignConnectionFactories/' + foreignConnFactName)
    cmo.setLocalJNDIName(localJNDIName)
    cmo.setRemoteJNDIName(remoteJNDIName)

    # Print output
    print('# Module Name: ' + moduleName )
    print('# Foreign Destination: ' + foreignConnFactName)
    print('# Local JNDI Name: ' + localJNDIName)
    print('# Remote JNDI Name: ' + remoteJNDIName)

    save()
    activate()

  except Exception, e:
    print e


def createQuota(line):
  try:
    startEdit()
    cd('/')
    items = line.split(',')
    items = [item.strip() for item in items]
    (type,moduleName,quotaName,bytesMaximum,messagesMaximum,policy,shared) = items
	
    # Check if JMS Module name correct
    redirect('/dev/null','false')
    modExist = ls('/JMSSystemResources/',returnMap='true')
    if moduleName not in modExist:
      print('!!! Wrong JMS Module Name :' + moduleName + ' !!!')
      exit(exitcode=1,defaultAnswer='y')
    
    # Check if Connection Factory already exist
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName )
    redirect('/dev/null','false')
    exist = ls('Quotas',returnMap='true')
    if quotaName in exist:
      print('!!! Quota ' + quotaName + ' already exist !!!!')
      exit(exitcode=1,defaultAnswer='y')
	  
    # Create Connection Factory
    cmo.createQuota(quotaName)
	
    cd('/JMSSystemResources/' + moduleName + '/JMSResource/' + moduleName + '/Quotas/' +quotaName)
    cmo.setBytesMaximum(long(bytesMaximum))
    cmo.setMessagesMaximum(long(messagesMaximum))
    cmo.setPolicy(policy)
    cmo.setShared(int(shared))

    # Print output
    print('# Module Name: ' + moduleName )
    print('# Quota: ' + quotaName )
    print('# Bytes Maximum: ' + str(bytesMaximum))
    print('# Message Maximum to : ' + str(messagesMaximum))
    print('# Policy: ' + str(policy))
    print('# Shared: ' + str(shared))

    save()
    activate()

  except Exception, e:
    print e

def main():
  propInputStream = FileInputStream(sys.argv[1])
  configProps = Properties()
  configProps.load(propInputStream)
   
  url=configProps.get("adminUrl")
  username=configProps.get("importUser")
  password=configProps.get("importPassword")
  csvLoc=configProps.get("csvLoc")
  
  connect(username , password , url)
  edit()
  file=open(csvLoc)
  for line in file.readlines():
    if line.strip().startswith('module'):
      print('======= Create JMS Module =======\n')
      createJMSModule(line)
      print('\n------- End of Create JMS Module -------\n\n')
	  
    elif line.strip().startswith('foreign'):
      print('======= Create Foreign Server =======\n')
      createForeignServer(line)
      print('\n------- End of Create Foreign Server -------\n\n')
	  
    elif line.strip().startswith('dest'):
      print('======= Create Foreign Destination =======\n')
      createForeignDest(line)
      print('\n------- End of Create Foreign Destination -------\n\n')
  
    elif line.strip().startswith('conn'):
      print('======= Create Foreign Connection Factory =======\n')
      createforeignConnFactName(line)
      print('\n------- End of Create Foreign Connection Factory -------\n\n')
	  
    elif line.strip().startswith('subdeployment'):
      print('======= Create Subdeployment =======\n')
      createSubdeploy(line)
      print('\n------- End of Create Subdeployment -------\n\n')
	  
    elif line.strip().startswith('queue'):
      print('======= Create Queue =======\n')
      createQueues(line)
      print('\n------- End of Create Queue -------\n\n')
	  
    elif line.strip().startswith('distqueueuniform'):
      print('======= Create Distributed Queue Uniform =======\n')
      createDistQueueUniform(line)
      print('\n------- End of Create Distributed Queue Uniform -------\n\n')
	  
    elif line.strip().startswith('distqueueweighted'):
      print('======= Create Distributed Queue Weighted =======\n')
      createDistQueueWeighted(line)
      print('\n------- End of Create Distributed Queue Weighted -------\n\n')
	  
    elif line.strip().startswith('topic'):
      print('======= Create Topic =======\n')
      createTopic(line)
      print('\n------- End of Create Topic -------\n\n')
	  
    elif line.strip().startswith('disttopicuniform'):
      print('======= Create Distributed Topic Uniform =======\n')
      createDistTopicUniform(line)
      print('\n------- End of Create Distributed Topic Uniform -------\n\n')
	  
    elif line.strip().startswith('disttopicweighted'):
      print('======= Create Distributed Topic Weighted =======\n')
      createDistTopicWeighted(line)
      print('\n------- End of Create Distributed Topic Weighted -------\n\n')
	  
    elif line.strip().startswith('factory'):
      print('======= Create Connection Factory =======\n')
      createConnFactory(line)
      print('\n------- End of Create Connection Factory -------\n\n')
	  
    elif line.strip().startswith('quota'):
      print('======= Create Quota =======\n')
      createQuota(line)
      print('\n------- End of Create Quota -------\n\n')
	  
    else:
      continue
	
  disconnect()

main()
	

