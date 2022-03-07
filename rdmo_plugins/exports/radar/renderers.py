from rdmo.core.renderers import BaseXMLRenderer


class RadarExportRenderer(BaseXMLRenderer):

    scheme_uri = {
        'INSI': 'http://www.isni.org/',
        'ORCID': 'https://orcid.org',
        'ROR': 'https://ror.org/',
        'GRID': 'https://www.grid.ac/'
    }

    def render_document(self, xml, dataset):
        xml.startElement('ns2:radarDataset', {
            'xmlns': 'http://radar-service.eu/schemas/descriptive/radar/v09/radar-elements',
            'xmlns:ns2': 'http://radar-service.eu/schemas/descriptive/radar/v09/radar-dataset'
        })

        # identifier
        identifier = dataset.get('identifier')
        if identifier:
            self.render_text_element(xml, 'identifier', {
                'identifierType': dataset.get('identifierType', 'OTHER')
            }, identifier)

        # creators
        creators = dataset.get('creators', {}).get('creator')
        if creators:
            xml.startElement('creators', {})
            for creator in creators:
                xml.startElement('creator', {})
                self.render_text_element(xml, 'creatorName', {}, creator.get('creatorName'))

                if creator.get('givenName'):
                    self.render_text_element(xml, 'givenName', {}, creator.get('givenName'))

                if creator.get('familyName'):
                    self.render_text_element(xml, 'familyName', {}, creator.get('familyName'))

                if creator.get('creatorAffiliation'):
                    self.render_text_element(xml, 'creatorAffiliation', {}, creator.get('creatorAffiliation'))

                name_identifier = creator.get('nameIdentifier')
                if name_identifier:
                    self.render_text_element(xml, 'nameIdentifier', {
                        'nameIdentifierScheme': name_identifier[0].get('nameIdentifierScheme'),
                    }, name_identifier[0].get('value'))

                xml.endElement('creator')
            xml.endElement('creators')

        # title
        title = dataset.get('title')
        if title:
            self.render_text_element(xml, 'title', {}, title)

        # publisher
        publisher = dataset.get('publishers', {}).get('publisher')
        if publisher:
            self.render_text_element(xml, 'publisher', {}, publisher[0])

        # productionYear
        production_year = dataset.get('productionYear')
        if production_year:
            self.render_text_element(xml, 'productionYear', {}, production_year)

        # publicationYear
        publication_year = dataset.get('publicationYear')
        if publication_year:
            self.render_text_element(xml, 'publicationYear', {}, publication_year)

        # subjectArea
        subject_areas = dataset.get('subjectAreas', {}).get('subjectArea')
        if subject_areas:
            xml.startElement('subjectAreas', {})
            for subject_area in subject_areas:
                xml.startElement('subjectArea', {})
                self.render_text_element(xml, 'controlledSubjectAreaName', {}, subject_area.get('controlledSubjectAreaName'))
                if subject_area.get('additionalSubjectAreaName'):
                    self.render_text_element(xml, 'additionalSubjectAreaName', {}, subject_area.get('additionalSubjectAreaName'))
                xml.endElement('subjectArea')
            xml.endElement('subjectAreas')

        # resource
        resource = dataset.get('resource')
        if resource:
            self.render_text_element(xml, 'resource', {
                'resourceType': resource.get('resourceType')
            }, resource.get('value'))

        # rights
        rights = dataset.get('rights')
        if rights:
            xml.startElement('rights', {})
            self.render_text_element(xml, 'controlledRights', {}, rights.get('controlledRights'))
            additional_rights = rights.get('additionalRights')
            if additional_rights:
                self.render_text_element(xml, 'additionalRights', {}, additional_rights)
            xml.endElement('rights')

        # rightsHolders
        rights_holders = dataset.get('rightsHolders', {}).get('rightsHolder')
        if rights_holders:
            xml.startElement('rightsHolders', {})
            for rights_holder in rights_holders:
                self.render_text_element(xml, 'rightsHolder', {}, rights_holder)
            xml.endElement('rightsHolders')

        # additionalTitles
        additional_titles = dataset.get('additionalTitles')
        if additional_titles:
            xml.startElement('additionalTitles', {})
            for additional_title in additional_titles:
                self.render_text_element(xml, 'additionalTitle', {
                    'additionalTitleType': additional_title['additionalTitleType']
                }, additional_title['additionalTitle'])
            xml.endElement('additionalTitles')

        # descriptions
        descriptions = dataset.get('descriptions', {}).get('description')
        if descriptions:
            xml.startElement('descriptions', {})
            for description in descriptions:
                self.render_text_element(xml, 'description', {
                    'descriptionType': description.get('descriptionType', 'ABSTRACT')
                }, description.get('value'))
            xml.endElement('descriptions')

        # keywords
        keywords = dataset.get('keywords')
        if keywords:
            xml.startElement('keywords', {})
            for keyword in keywords:
                self.render_text_element(xml, 'keyword', {}, keyword)
            xml.endElement('keywords')

        # contributors
        contributors = dataset.get('contributors', {}).get('contributor')
        if contributors:
            xml.startElement('contributors', {})
            for contributor in contributors:
                print(contributor)
                xml.startElement('contributor', {})
                self.render_text_element(xml, 'contributorName', {}, contributor.get('contributorName'))

                if contributor.get('givenName'):
                    self.render_text_element(xml, 'givenName', {}, contributor.get('givenName'))

                if contributor.get('familyName'):
                    self.render_text_element(xml, 'familyName', {}, contributor.get('familyName'))

                if contributor.get('contributorAffiliation'):
                    self.render_text_element(xml, 'contributorAffiliation', {}, contributor.get('contributorAffiliation'))

                name_identifier = contributor.get('nameIdentifier')
                if name_identifier:
                    self.render_text_element(xml, 'nameIdentifier', {
                        'nameIdentifierScheme': name_identifier[0].get('nameIdentifierScheme'),
                    }, name_identifier[0].get('value'))

                xml.endElement('contributor')
            xml.endElement('contributors')

        # language
        language = dataset.get('language')
        if language:
            self.render_text_element(xml, 'language', {}, language)

        # resource_type
        resource_type = dataset.get('resourceType')
        if resource_type:
            self.render_text_element(xml, 'resourceType', {
                'resourceTypeGeneral': dataset.get('resourceTypeGeneral')
            }, resource_type)

        # alternate_identifiers
        alternate_identifiers = dataset.get('alternateIdentifiers', {}).get('alternateIdentifier')
        if alternate_identifiers:
            xml.startElement('alternateIdentifiers', {})
            for alternate_identifier in alternate_identifiers:
                self.render_text_element(xml, 'alternateIdentifier', {
                    'alternateIdentifierType': alternate_identifier.get('alternateIdentifierType')
                }, alternate_identifier.get('value'))
            xml.endElement('alternateIdentifiers')

        # related_identifiers
        related_identifiers = dataset.get('relatedIdentifiers', {}).get('relatedIdentifier')
        if related_identifiers:
            xml.startElement('relatedIdentifiers', {})
            for related_identifier in related_identifiers:
                self.render_text_element(xml, 'relatedIdentifier', {
                    'relatedIdentifierType': related_identifier.get('relatedIdentifierType'),
                    'relationType': related_identifier.get('relationType')
                }, related_identifier.get('value'))
            xml.endElement('relatedIdentifiers')

        # dataSources
        data_sources = dataset.get('dataSources', {}).get('dataSource')
        if data_sources:
            xml.startElement('dataSources', {})
            for data_source in data_sources:
                self.render_text_element(xml, 'dataSource', {
                    'dataSourceDetail': data_source.get('dataSourceDetail')
                }, data_source.get('value'))
            xml.endElement('dataSources')

        # software
        software = dataset.get('software')
        if software:
            xml.startElement('software', {})
            for software_type in software:
                xml.startElement('softwareType', {
                    'type': software_type.get('type')
                })
                self.render_text_element(xml, 'softwareName', {
                    'softwareVersion': software_type.get('softwareVersion')
                }, software_type.get('softwareName'))
                if 'alternativeSoftwareName' in software_type:
                    self.render_text_element(xml, 'alternativeSoftwareName', {
                        'alternativeSoftwareVersion': software_type.get('alternativeSoftwareVersion')
                    }, software_type.get('alternativeSoftwareName'))
                xml.endElement('softwareType')
            xml.endElement('software')

        # processing
        processing_list = dataset.get('dataProcessing')
        if processing_list:
            xml.startElement('processing', {})
            for processing in processing_list:
                self.render_text_element(xml, 'dataProcessing', {}, processing)
            xml.endElement('processing')

        # relatedInformations
        related_informations = dataset.get('relatedInformations')
        if related_informations:
            xml.startElement('relatedInformations', {})
            for related_information in related_informations:
                self.render_text_element(xml, 'relatedInformation', {
                    'relatedInformationType': related_information.get('relatedInformationType')
                }, related_information.get('relatedInformation'))
            xml.endElement('relatedInformations')

        # funding_references
        funding_references = dataset.get('fundingReferences', {}).get('fundingReference')
        if funding_references:
            xml.startElement('fundingReferences', {})
            for funding_reference in funding_references:
                xml.startElement('fundingReference', {})
                self.render_text_element(xml, 'funderName', {}, funding_reference.get('funderName'))
                if funding_reference.get('funderIdentifier'):
                    self.render_text_element(xml, 'funderIdentifier', {
                        'type': funding_reference.get('funderIdentifier').get('type')
                    }, funding_reference.get('funderIdentifier').get('value'))
                if funding_reference.get('awardNumber'):
                    self.render_text_element(xml, 'awardNumber', {}, funding_reference.get('awardNumber'))
                if funding_reference.get('awardURI'):
                    self.render_text_element(xml, 'awardURI', {}, funding_reference.get('awardURI'))
                if funding_reference.get('awardTitle'):
                    self.render_text_element(xml, 'awardTitle', {}, funding_reference.get('awardTitle'))
                xml.endElement('fundingReference')
            xml.endElement('fundingReferences')

        xml.endElement('ns2:radarDataset')
